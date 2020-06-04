# WEBCLIM

[WebClim](https://medialab.sciencespo.fr/activites/webclim/) is a research project in Sciences Po's medialab. Our goal is to analyze the fake news ecosystem about climate change, and other scientific topics, on Facebook, Twitter, Youtube, and other platforms. 

This repo is used to create the last two figures of [this chronicle](https://medialab.sciencespo.fr/actu/les-infox-sur-le-covid-sous-surveillance/) (in French).

### Set up

This project was developed on Python 3.7.6, so you should first install Python. 
Then run these commands in your terminal (in a virtualenv if you prefer):

```
git clone https://github.com/medialab/webclim_temporal_evolution_facebook
cd webclim_temporal_evolution_facebook
pip install -r requirements.txt
```

### Collect the CrowdTangle data

You should have a CrowdTangle token and write it in a `config.json` file similar to the `config.json.example` file 
(except that you should write the token value instead of "blablabla").

You should also add a list of Facebook groups and add each group manually to the list. You can get all your list ids id with:
```
token_crowdtangle=$(jq -r '.token_crowdtangle' config.json)
minet ct lists --token $token_crowdtangle
```

To get all the posts of these Facebook groups, you should run this:
```
DATE="2020_06_04"
DATA_DIRECTORY="data"
OUTPUT_FILE="./${DATA_DIRECTORY}/posts_groups_${DATE}.csv"

minet ct posts --token $token_crowdtangle --list-ids 1401873 --start-date 2019-09-01 \
  --rate-limit 50 --partition-strategy 500 > $OUTPUT_FILE
```
(Precising a start date is mandatory.)

### Replicate the [chronicle's figures](https://medialab.sciencespo.fr/actu/les-infox-sur-le-covid-sous-surveillance/)

To save the two graphs and print a sump-up table:
```
python ./src/plot_temporal_evolution.py
```
