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

### Cloud Build

For reasons beyond my comprehension, the docker image created by Cloud Build did not deploy correctly. Running
the build locally (even using the cloud-build-local tool) worked fine, but GCP builds could not find the structure
of logs files and directories. As a result I took out logging as there wasn't much going on anyway. 

There are also two Dockerfiles in the code. The first is the original, and contains all the commands for 
downloading and running Chrome and the Chromedriver. This adds a lot of bloat to the image and I consequently
made a second version that only contains the python code for reading and displaying the data. No scraping has 
happened since around Sept-Oct 2021. 
