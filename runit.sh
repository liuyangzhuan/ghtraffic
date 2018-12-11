module load python
cd /global/homes/l/liuyangz/Cori/my_research/ghtraffic
git pull
python ./ghtraffic.py
git add *.org
git commit -m "weekly update"
git push


