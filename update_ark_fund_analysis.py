import pickle
from pathlib import Path
from datetime import datetime
import pytz
import os
import subprocess

utc = pytz.utc
time_format = '%Y-%m-%d %H:%M:%S %z'
base_dir = Path(__file__).parent.absolute()
exported_notebook_path = base_dir / '../ark_fund_analysis/output/ark_fund_analysis.html'

# Check when notebook was last exported
if os.path.isfile(exported_notebook_path):
    notebook_exported = datetime.fromtimestamp(os.path.getmtime(exported_notebook_path)).replace(tzinfo=utc)
else:
    notebook_exported = None

website_updated_path = base_dir / 'ignore/website_updated.p'

# Make `ignore` directory if it doesn't exist
if not os.path.exists(os.path.dirname(website_updated_path)):
    os.makedirs(os.path.dirname(website_updated_path))

# Check when website was last updated
if os.path.isfile(website_updated_path):
    with open(website_updated_path, 'rb') as handle:
        website_updated = pickle.load(handle)
else:
    website_updated = None

if notebook_exported is None or website_updated is None or notebook_exported > website_updated:
    git_path = '/usr/bin/git'
    website_repo = Path('/home/ubuntu/depasqualexyz.github.io/')
    website_root = website_repo / 'docs'
    notebook_dest_path = website_root / 'ark-fund-analysis/index.html'
    timestamp = datetime.now().astimezone(utc).strftime(time_format) # Equivalent shell command: date -u +"%Y-%m-%d %H:%M:%S %z"
    command = f"cd {website_repo} && {git_path} pull && cp '{exported_notebook_path}' '{notebook_dest_path}' && {git_path} add -A && {git_path} commit -m 'Update ARK Fund Analysis ({timestamp})' && {git_path} push"
    subprocess.run(command, shell=True, check=True)
    with open(website_updated_path, 'wb') as handle:
        pickle.dump(notebook_exported, handle)
