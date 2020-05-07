#! /bin/sh

. /opt/modules/default/etc/modules.sh
module load python/3.7-anaconda-2019.10 
cd /project/projectdirs/m2957/liuyangz/my_research/ghtraffic
git pull
python ./ghtraffic.py
git add *.org
git commit -m "weekly update"
git push


