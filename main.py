import requests as r
import json
from typing import List, Dict, Set
from cli import namespace
import subprocess


def fetch_packages(url: str) -> List[Dict]:
    return r.get(url=url).json()["packages"]


def architecture_defining(packages: List[Dict]) -> List[str]:
    architecture = []
    for package in packages:
        if package["arch"] not in architecture:
            architecture.append(package["arch"])
    return architecture


def group_packages_by_arch(
    architectures: List[str],
    packages: List[Dict],
) -> Dict[str, List[Dict]]:
    sorted_packages = {arch: [] for arch in architectures}

    for arch in sorted_packages.keys():
        for package in packages:
            if package["arch"] == arch:
                sorted_packages[arch].append(package)
    return sorted_packages


def compare_packages_by_arch(
    architectures: Set[str],
    branch_1_name: str,
    branch_2_name: str,
    branch_1: Dict[str, List[Dict]],
    branch_2: Dict[str, List[Dict]],
) -> Dict[str, Dict]:

    output_structure = {
        arch: {
            f"Unique_packages_of_{branch_2_name}": [],
            f"Unique_packages_of_{branch_1_name}": [],
            f"Packages_with_newer_version_release_in_{branch_1_name}": [],
        }
        for arch in architectures
    }

    def package_key(package: Dict) -> str:
        # Unique package identifier for efficient lookup and comparison.
        return f"{package['name']}-{package['epoch']}-{package['version']}-{package['release']}--{package['arch']}"

    for arch_name, packages in branch_1.items():
        if arch_name not in branch_2:
            output_structure[arch_name][f"Unique_packages_of_{branch_1_name}"].extend(
                packages
            )
        else:
            unique_packages_branch_2 = {package_key(p) for p in branch_2[arch_name]}
            for package in packages:
                if package_key(package) not in unique_packages_branch_2:
                    output_structure[arch_name][
                        f"Unique_packages_of_{branch_1_name}"
                    ].append(package)

    for arch_name, packages in branch_2.items():
        if arch_name not in branch_1:
            output_structure[arch_name][f"Unique_packages_of_{branch_2_name}"].extend(
                packages
            )
        else:
            unique_packages_branch_1 = {package_key(p) for p in branch_1[arch_name]}
            for package in packages:
                if package_key(package) not in unique_packages_branch_1:
                    output_structure[arch_name][
                        f"Unique_packages_of_{branch_2_name}"
                    ].append(package)

    def compare_versions(version1, version2, cache={}):
        if (version1, version2) in cache:
            # Use cached result if available to avoid re-calculating
            return cache[(version1, version2)]
        try:
            result = subprocess.run(
                ["rpmdev-vercmp", version1, version2],
                capture_output=True,
                text=True,
            )
            output = result.stdout.strip()

            if version1 + " > " + version2 in output:
                comparison_result = 1
            elif version1 + " < " + version2 in output:
                comparison_result = -1
            elif version1 + " == " + version2 in output:
                comparison_result = 0
            else:
                print(f"Unexpected output of rpmdev-vercmp: {output}")
                comparison_result = None

            cache[(version1, version2)] = comparison_result
            return comparison_result

        except subprocess.CalledProcessError as e:
            print(f"Error with rpmdev-vercmp: {e.stderr}")
            return None

    for arch_name in architectures:
        if arch_name in branch_1 and arch_name in branch_2:

            branch_1_packages_by_name = {p["name"]: p for p in branch_1[arch_name]}
            branch_2_packages_by_name = {p["name"]: p for p in branch_2[arch_name]}

            common_package_names = set(branch_1_packages_by_name.keys()) & set(
                branch_2_packages_by_name.keys()
            )

            for package_name in common_package_names:
                package_1 = branch_1_packages_by_name[package_name]
                package_2 = branch_2_packages_by_name[package_name]

                # Making structure suitable for rpmdev-vercmp comparison
                version1 = package_1["version"] + "-" + package_1["release"]
                version2 = package_2["version"] + "-" + package_2["release"]

                comparison_result = compare_versions(version1, version2)

                if comparison_result is not None and comparison_result > 0:
                    output_structure[arch_name][
                        f"Packages_with_newer_version_release_in_{branch_1_name}"
                    ].append(package_1)

    return output_structure


if __name__ == "__main__":
    try:
        name_of_1_branch = namespace.branches[0]
        name_of_2_branch = namespace.branches[1]

        URL1 = f"https://rdb.altlinux.org/api/export/branch_binary_packages/{name_of_1_branch}"
        URL2 = f"https://rdb.altlinux.org/api/export/branch_binary_packages/{name_of_2_branch}"

        packages_of_1_branch = fetch_packages(URL1)
        packages_of_2_branch = fetch_packages(URL2)

        arch_of_1_branch = architecture_defining(packages_of_1_branch)
        arch_of_2_branch = architecture_defining(packages_of_2_branch)

        sorted_1_branch = group_packages_by_arch(arch_of_1_branch, packages_of_1_branch)
        sorted_2_branch = group_packages_by_arch(arch_of_2_branch, packages_of_2_branch)

        all_architecture_types = set(arch_of_1_branch) | set(arch_of_2_branch)

        report = compare_packages_by_arch(
            all_architecture_types,
            name_of_1_branch,
            name_of_2_branch,
            sorted_1_branch,
            sorted_2_branch,
        )

        if namespace.output == "terminal":
            print(report, end="\n")
        else:
            with open(namespace.output, "w") as f:
                json.dump(report, f, indent=4)

    except Exception as e:
        print(f"An error: {e}")
