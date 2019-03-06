#!/bin/bash
/usr/local/bin/python3 /Users/frontend/bot/manage.py update-beauty

/bin/date >> /tmp/crontab_log
echo "beauty updated" >> /tmp/crontab_log
