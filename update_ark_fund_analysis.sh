: '
Crontab entry:

# Every 15 minutes (starting at minute 2)
PYTHON_PATH=/home/ubuntu/miniconda3/bin/python
ARK_FUND_ANALYSIS=/home/ubuntu/ark_fund_analysis
WEBSITE_REPO=/home/ubuntu/a-dpq.github.io
SUBJECT="Error from cron job: download ARK data"
2-59/15 * * * * (/usr/bin/bash $WEBSITE_REPO/update_ark_fund_analysis.sh) 2> $ARK_FUND_ANALYSIS/output/cron_stderr.log 1> $ARK_FUND_ANALYSIS/output/cron_stdout.log || $PYTHON_PATH /home/ubuntu/send_email/send_email.py "$SUBJECT" < $ARK_FUND_ANALYSIS/output/cron_stderr.log
'

PYTHON_PATH=/home/ubuntu/miniconda3/bin/python
GIT_PATH=/usr/bin/git
ARK_FUND_ANALYSIS=/home/ubuntu/ark_fund_analysis
WEBSITE_REPO=/home/ubuntu/a-dpq.github.io

# Check for new data and export the notebook
cd $ARK_FUND_ANALYSIS && $PYTHON_PATH cron_export_notebook.py
# Upload exported notebook to website
cd $WEBSITE_REPO && $PYTHON_PATH update_ark_fund_analysis.py
# Update data repository and upload
cd $ARK_FUND_ANALYSIS/data/ark_fund_holdings && $GIT_PATH pull && $GIT_PATH add -A && $GIT_PATH commit -m 'Add new data from server' && $GIT_PATH push
