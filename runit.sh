#! /bin/sh

. /opt/modules/default/etc/modules.sh
module load python/2.7-anaconda-2019.07
cd /global/homes/l/liuyangz/Cori/my_research/ghtraffic
git pull
python ./ghtraffic.py
git add *.org
git commit -m "weekly update"
git push


