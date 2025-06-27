import pytest
from main import fetch_packages, architecture_defining, group_packages_by_arch


@pytest.fixture
def correct_url():
    return "https://rdb.altlinux.org/api/export/branch_binary_packages/sisyphus"


@pytest.fixture
def incorrect_url():
    return "https://rdb.linuxalt.org/api/export/branch_binary_packages/sisyphus"


@pytest.fixture
def correct_packages():
    return [
        {
            "name": "389-ds-base-libs-debuginfo",
            "epoch": 0,
            "version": "3.1.2",
            "release": "alt2",
            "arch": "aarch64",
            "disttag": "sisyphus+373095.200.3.1",
            "buildtime": 1738752825,
            "source": "389-ds-base",
        },
        {
            "name": "xwininfo-debuginfo",
            "epoch": 0,
            "version": "1.1.5",
            "release": "alt1",
            "arch": "x86_64",
            "disttag": "sisyphus+237156.100.1.1",
            "buildtime": 1567686617,
            "source": "xwininfo",
        },
    ]


@pytest.fixture
def incorrect_packages():
    return [
        {
            "name": "389-ds-base-libs-debuginfo",
            "epoch": 0,
            "source": "389-ds-base",
        },
        {
            "version": "1.1.5",
            "release": "alt1",
            "disttag": "sisyphus+237156.100.1.1",
        },
    ]


def test_correct_fetching_packages(correct_url):
    branch_packages = fetch_packages(correct_url)
    assert branch_packages[0] == {
        "name": "0ad",
        "epoch": 1,
        "version": "0.27.0",
        "release": "alt2",
        "arch": "aarch64",
        "disttag": "sisyphus+383316.70.4.1",
        "buildtime": 1746599998,
        "source": "0ad",
    }


def test_incorrect_fetching_packages(incorrect_url):
    with pytest.raises(Exception):
        fetch_packages(incorrect_url)


def test_correct_architecture_defining(correct_packages):
    arch = architecture_defining(correct_packages)
    assert arch == ["aarch64", "x86_64"]


def test_incorrect_architecture_defining(incorrect_packages):
    with pytest.raises(KeyError):
        architecture_defining(incorrect_packages)


def test_correct_grouping_packages_by_arc(correct_packages):
    arch = architecture_defining(correct_packages)
    sorted_branch = group_packages_by_arch(arch, correct_packages)
    assert sorted_branch == {
        "aarch64": [
            {
                "name": "389-ds-base-libs-debuginfo",
                "epoch": 0,
                "version": "3.1.2",
                "release": "alt2",
                "arch": "aarch64",
                "disttag": "sisyphus+373095.200.3.1",
                "buildtime": 1738752825,
                "source": "389-ds-base",
            }
        ],
        "x86_64": [
            {
                "name": "xwininfo-debuginfo",
                "epoch": 0,
                "version": "1.1.5",
                "release": "alt1",
                "arch": "x86_64",
                "disttag": "sisyphus+237156.100.1.1",
                "buildtime": 1567686617,
                "source": "xwininfo",
            }
        ],
    }
