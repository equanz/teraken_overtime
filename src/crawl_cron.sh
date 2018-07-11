#!/bin/sh

crawl_script="*/5 * * * * python $1" # script(you have to set arg)
crawl_script_delete="\*\/5 \* \* \* \* python $1" # script(you have to set arg)

crontab -l > $HOME/teraken_overtime_dump/crontab.txt # save crontab file
if [ $? = 0 ]; then # cron task is exist
    sed -i -e '/^'"$crawl_script_delete"'/d' $HOME/teraken_overtime_dump/crontab.txt # delete script
    sed -i -e '$a\
    '"$crawl_script"'' $HOME/teraken_overtime_dump/crontab.txt # add script
else
    echo "$crawl_script" >> $HOME/teraken_overtime_dump/crontab.txt
fi

crontab $HOME/teraken_overtime_dump/crontab.txt # set to crontab

