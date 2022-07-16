install: 
	pip install --upgrade pip &&\
		pip install -r requirements.txt

config:
	source ~/.virtualenvs/vax-service/bin/activate
	
lint: 
	pylint --disable=R,C *.py *.py lib/*.py

format:
	black *.py lib/*.py

all: install lint format
