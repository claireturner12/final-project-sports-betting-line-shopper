# final-project-sports-betting-line-shopper
This final project allows you to shop for the best sports betting lines using the-odds-api as the data gathering tool.

# Api Key:
- THE_ODDS_API is saved in the .env file

# Setup 
## Virtual Environment Setup
Create and activate a Conda virtual environment:

```bash
conda create -n betting-env python=3.11
conda activate betting-en
```

## Clone repo and download it from github. Navigate to repo from commandline: here's an example
cd ~/Users/alexanderbotticelli/Documents/GitHub

## Install Dependencies

```bash
pip install -r requirements.txt
```

# Testing
pytest

# install requirements (do this first to run app)
pip install -r requirements.txt

# run website (do this second to run app)
FLASK_APP=web_app flask run