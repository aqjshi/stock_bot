A Django-based stock trading bot using TimescaleDB, Polygon, Alpha Vantage, and more.

Tech Stack
Python 3.12
GitHub
Django
GitHub
bash
Copy
pip install "Django>=5.1,<5.2"
TimescaleDB Cloud
Learn more (or use the Docker version)
Django Timescaledb
GitHub
bash
Copy
pip install django-timescaledb
Python Requests
GitHub
bash
Copy
pip install requests
Jupyter
Official Site
bash
Copy
pip install jupyter
Psycopg (Binary Release)
PyPI
bash
Copy
pip install "psycopg[binary]"
Python Decouple
GitHub
Loads environment variables (e.g., from a .env file) with type casting and defaults.
Polygon.io
Website | Docs
Alpha Vantage
Website | Docs
OpenAI
Website
Tutorials
In-depth Setup
Watch on YouTube
Django Setup for Jupyter Notebooks (Short + Code)
View Tutorial
Full Tutorial
Watch on YouTube
Getting Started
Prerequisites
Download and install the following:

Git
VSCode (or Cursor)
Docker Desktop or Docker Engine (Linux install script)
Python
Clone the Repository
bash
Copy
git clone https://github.com/aqjshi/stock_bot.git
Environment Setup
Create an Environment File

bash
Copy
touch .env
Populate .env with your keys (e.g., ALPHA_VANTAGE_API_KEY="CSZDVN7BYPHHRPF4").

Initialize Git

bash
Copy
git checkout start
rm -rf .git
git init
git add --all
git commit -m "It's my bot now"
Create a Python Virtual Environment

macOS/Linux/WSL:
bash
Copy
python3.12 -m venv venv
source venv/bin/activate
Windows (PowerShell):
powershell
Copy
c:\Path\To\Python312\python.exe -m venv venv
.\venv\Scripts\activate
Install Requirements

bash
Copy
(venv) python -m pip install -r requirements.txt
Start Docker Containers

For local TimescaleDB and Redis:

bash
Copy
docker compose -f compose.yaml up -d
Django Setup
Create a Superuser

bash
Copy
python src/manage.py createsuperuser
Apply Migrations

bash
Copy
python src/manage.py makemigrations
python src/manage.py migrate
Run the Development Server

bash
Copy
python src/manage.py runserver
Open the provided URL in your browser and log in.

Data Generation & Bulk Loading
Polygon API:
Complete dataset generation, local data structure, and SQLite query have been implemented.
Data Storage:
Data is stored locally in src/db.sqlite3. The bulk load notebook (bulk_load.ipynb) generates between 20–80 MB of data, depending on your operating system.
Testing Environment:
Use the alpha_vantage_bulk_load.ipynb notebook to test and verify API integrations and batch processing.
Tip: Restart the Jupyter kernel after modifying functions to clear cached variables.
Next Steps
Alpha Vantage Integration:

Migrate Polygon subfunctions to Alpha Vantage.
Update the alpha_vantage.py file.
Verify working URLs and technical indicators.
Run makemigrations and migrate to update the data structure.
Project Tasks:

Hailey: Focus on Alpha Vantage API integration.
Anthony:
Part 1: Train/Validation/Test set creation, model implementation, and evaluation.
Part 2: Optimize window size and evaluate Sharpe ratio.
Additional Tools
Converting Markdown/Text to a Jupyter Notebook
To convert a Python script (or Markdown text) into a Jupyter Notebook using Jupytext:

bash
Copy
jupytext --to notebook nbs/build_dataset.py
