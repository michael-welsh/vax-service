[![Test Multiple Python Versions](https://github.com/michael-welsh/vax-service/actions/workflows/main.yml/badge.svg)](https://github.com/michael-welsh/vax-service/actions/workflows/main.yml)

# Vax Service
This project is the backend for the service that scrapes Hong Kong vaccination stats from the government website, and presents them in pretty graphs. 

At the time of creation of this project, there was oddly no other site providing this information in graphical format. Ths whole project is of course outdated, but serves as a quick example of using python-based data scraping tools and some Angular-based graph packages 


### Stack

This is a python app that originally called a MySQL database. The data layer was later migrated to Cloud Datastore as it was cheaper to run and something new to do. 

The python app is containerized and is built using GCP Cloud Build. Any commits to this repository will spark a new build and new version. 

### Setup
1. Create a virtualenv - `python3 -m / ~/.virtualenvs/vax-service`
2. Modify the .bashrc `source ~/.virtualenvs/vax-service/bin/activate`
3. clone project then run `make all`

### Project Scaffold

Build out python project scaffold:

* [Makefile](https://github.com/michael-welsh/vax-service/blob/main/Makefile)
* [requirements.txt](https://github.com/michael-welsh/vax-service/blob/main/requirements.txt)
* [Dockerfile](https://github.com/michael-welsh/vax-service/blob/main/Dockerfile)
* command-line-tool
* Microservice



