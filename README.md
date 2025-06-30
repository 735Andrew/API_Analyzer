<h2 style="text-align: center;">API Analyzer</h2>
<br>
<b>API Analyzer</b> - a special utility that helps to compare binary packages in repositories.
<br><br><br>
:arrow_down_small:<b>Key Features</b>:arrow_down_small:
<ul>
    <li>Architecture is flexible for different types of branches.</li>
    <li>Packages are compared using a specialized RPM versioning scheme.</li>
    <li>The program has user-friendly CLI-utility.</li>
</ul>
<hr>
<div>
<h3 style="text-align: center;">Installation on RedHat-based operating systems</h3>
<h6>Prerequisites:</h6>

```bash
sudo yum -y update
sudo yum -y install python3 git
sudo yum -y install rpmdevtools  
```

<h6>Project deployment</h6>

```bash
git clone https://github.com/735Andrew/API_Analyzer
cd API_Analyzer 
python3 -m venv venv 
source venv/bin/activate 
(venv) pip install -r requirements.txt
    
(venv) python3 main.py --branches sisyphus p10 --output data.txt    # Data output of branches sisyphus & p10 into file in root directory
(venv) python3 main.py -b p9 p11 -o terminal                        # Data output of branches p9 & p11 into terminal
    
```
</div>
<hr>