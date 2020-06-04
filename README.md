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

You should have a CrowdTangle account and write it in a `config.json` file similar to the `config.json.example` file 
(except that you should write the token value instead of "blablabla").

You should first clean the Science Feedback data, and then do the CrowdTangle request. For example, if you want the fake news about climate change (the second command will take 1-2 hours to run):
```
python ./src/clean_data.py climate 15_05_2020
./src/minet_requests.sh climate 15_05_2020
```
