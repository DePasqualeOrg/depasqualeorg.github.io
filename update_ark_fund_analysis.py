'''
Run `crontab -e` and add the following (with correct paths) to check for new data every 15 minutes (starting at minute 2) and export the notebook, and update the website when new data is downloaded.
PYTHON_PATH=/home/ubuntu/miniconda3/bin/python
ARK_FUND_ANALYSIS=/home/ubuntu/ark_fund_analysis
WEBSITE_REPO=/home/ubuntu/a-dpq.github.io
COMMAND="cd $ARK_FUND_ANALYSIS && $PYTHON_PATH cron_export_notebook.py && cd $WEBSITE_REPO && $PYTHON_PATH update_ark_fund_analysis.py"
2-59/15 * * * * (eval $COMMAND) 2>> $ARK_FUND_ANALYSIS/output/cron_stderr.log 1> $ARK_FUND_ANALYSIS/output/cron_stdout.log
'''

import pickle
from pathlib import Path
from datetime import datetime
import pytz
import os
import subprocess
from os import path

utc = pytz.utc
time_format = '%Y-%m-%d %H:%M:%S %z'
base_dir = Path(__file__).parent.absolute()
exported_notebook_path = base_dir / '../ark_fund_analysis/output/ark_fund_analysis.html'

if os.path.isfile(exported_notebook_path):
    notebook_updated = datetime.fromtimestamp(os.path.getmtime(exported_notebook_path)).replace(tzinfo=utc).strftime(time_format)
else:
    notebook_updated = None

notebook_previously_updated_path = base_dir / 'notebook_previously_updated.p'

if os.path.isfile(notebook_previously_updated_path):
    with open(notebook_previously_updated_path, 'rb') as handle:
        notebook_previously_updated = pickle.load(handle)
else:
    notebook_previously_updated = None

# !! Check if previous updated time has been saved, and if so, compare to notebook_updated
# !! If notebook_updated > previous saved time, or no saved time is found, run the following:

print(f'Notebook updated: {notebook_updated}')
print(f'Notebook previously updated: {notebook_previously_updated}')

if notebook_previously_updated is None or notebook_updated > notebook_previously_updated:
    git_path = '/usr/bin/git'
    website_repo = Path('/home/ubuntu/a-dpq.github.io/')
    website_root = website_repo / 'docs'
    notebook_dest_path = path.join(website_root, 'ark-fund-analysis/index.html')
    timestamp = datetime.now().astimezone(utc).strftime(time_format) # Equivalent shell command: date -u +"%Y-%m-%d %H:%M:%S %z"

    command = f"cd {website_repo} && {git_path} pull && cp '{exported_notebook_path}' '{notebook_dest_path}' && {git_path} add -A && {git_path} commit -m 'Update {timestamp}' && {git_path} push"

    # try:
    #     subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    # except subprocess.CalledProcessError as e:
    #     raise RuntimeError(f"Command '{e.cmd}' returned with error (code {e.returncode}): {e.output}")

    subprocess.run(command, shell=True, check=True)

    with open(notebook_previously_updated_path, 'wb') as handle:
        pickle.dump(notebook_updated, handle)
