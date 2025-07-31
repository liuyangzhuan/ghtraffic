#! /bin/sh

module load python
cd /global/cfs/cdirs/m2957/liuyangz/my_research/ghtraffic
git pull
python ./ghtraffic.py
git add *.org
git commit -m "weekly update"
git push


