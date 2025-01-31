__Tech Stack__
- [Python 3.12](https://github.com/python)
- [Django](https://github.com/django/django) (`pip install "Django>=5.1,<5.2"`)
- [TimescaleDB Cloud](https://tsdb.co/justin) (or Docker version)
- [Django Timescaledb](https://github.com/jamessewell/django-timescaledb) (`pip install django-timescaledb`)
- [Python requests](https://github.com/psf/requests) (`pip install requests`)
- [Jupyter](https://jupyter.org/) (`pip install jupyter`)
- [Psycopg Binary Release](https://pypi.org/project/psycopg/) (`pip install "psycopg[binary]"`)
- [Python Decouple](https://github.com/HBNetwork/python-decouple) to load environment variables (e.g. `.env`) with type casting and default values.
- [Polygon.io](https://polygon.io/?utm_source=cfe&utm_medium=github&utm_campaign=cfe-github) ([docs](https://polygon.io/docs/stocks/getting-started?utm_source=cfe&utm_medium=github&utm_campaign=cfe-github))
- [Alpha Vantage](https://www.alphavantage.co/?utm_source=cfe&utm_medium=github&utm_campaign=cfe-github) ([docs](https://www.alphavantage.co/documentation/?utm_source=cfe&utm_medium=github&utm_campaign=cfe-github))
- [OpenAI](https://www.openai.com/?utm_source=cfe&utm_medium=github&utm_campaign=cfe-github)

## Tutorial
- In-depth setup [on YouTube (https://youtu.be/aApDye1TWJ4)](https://youtu.be/aApDye1TWJ4)
- [Django Setup for use in Jupyter Notebooks (short + code)](https://www.codingforentrepreneurs.com/shorts/django-setup-for-use-in-jupyter-notebooks)
- Full tutorial [on YouTube (https://youtu.be/O3O1z5hTdUM)](https://youtu.be/O3O1z5hTdUM)

## Getting Started

Download the following:
- [git](https://git-scm.com/)
- [VSCode](https://code.visualstudio.com/) (or [Cursor](https://cursor.com/))
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine via [get.docker.com](https://get.docker.com/) (Linux Install Script)
- [Python](https://www.python.org/downloads/)

Documentation

Accomplished:

**POLYGON API**
- Generation of complete dataset
- Working Local datastructure and SQLlite Query

# API services
`ALPHA_VANTAGE_API_KEY="CSZDVN7BYPHHRPF4"`

**TO DO:**
- Hailey
  - ALPHA VANTAGE API
  - Checkout new branch
  - Look at Alpha Vantage API documentation

- Open docker desktop app, docker compose up -d
- Run `src/manage.py createsuperuser` (if not created already, otherwise cancel)
- Run `src/manage.py runserver` and copy the URL from the output, then login.

- Data is stored locally in a file called `src/db.sqlite3`
- `bulk_load.ipynb` creates around 20-80 MB of data (varies on operating system)
- Create a testing environment in Jupyter—you will thank me later—using `alpha_vantage_bulk_load.ipynb`. Copy the bulk load and the entire contents of the Polygon API into a new cell at the top to see how load balancing and batch processing work.
- Every variable is cached until you restart the kernel. If you modify a function or variable, refresh the kernel to avoid unexpected outputs due to cached values. Use print statements to speed up debugging.
- Once you adapt the Polygon subfunctions into Alpha Vantage subfunctions and they work correctly, paste them into the `alpha_vantage.py` file and tidy up the `alpha_vantage_bulk_load.ipynb`.
- After verifying all working URLs (some indicators might not work, which is acceptable), create a new variable for each “technical indicator” in the documentation in the format:  
  `f"alpha_vantage_{indicator_item}" = decimal item`  
- COMMENT OUT and LABEL which ones do not work. Then run `makemigrations` and `migrate` as per the GitHub documentation. Once completed, run `runserver` and verify updates in the data structure by checking the stock quote and its data items.
- Once you finish `alpha_vantage_bulk_load.ipynb`, `alpha_vantage.py`, and `src/market/models.py` and confirm everything works, get paid—225 for 15 hours of work. Faster completion equals higher pay.

**Anthony**
- Part 1:
  - Train/validation/test set section 1
  - Train/validation/test set section 2
  - Model implementation
  - Evaluation of model performance

- Part 2:
  - Section 2: Mining for optimal k window size
  - Evaluation of Sharpe ratio

## HOW TO TURN MARKDOWN TEXT INTO A JUPYTER NOTEBOOK
```bash
jupytext --to notebook nbs/build_dataset.py
[jupytext] Reading nbs/build_dataset.py in format py
[jupytext] Writing nbs/build_dataset.ipynb
```

Open a command line (Terminal, VSCode Terminal, Cursor Terminal, PowerShell, etc.)

Clone this Repo:
```bash
git clone https://github.com/aqjshi/stock_bot.git
```

Create your env file and populate it with keys:
```bash
touch .env 
```

Checkout the start branch:
```bash
git checkout start
rm -rf .git
git init
git add --all
git commit -m "It's my bot now"
```

Create a Python virtual environment:

_macOS/Linux/WSL_
```bash
python3.12 -m venv venv
source venv/bin/activate
```

_Windows PowerShell_
```powershell
c:\Path\To\Python312\python.exe -m venv venv
.\venv\Scripts\activate
```

Install requirements:
```bash
(venv) python -m pip install -r requirements.txt
```

Docker Compose Up (for local TimescaleDB and Redis):
```bash
docker compose -f compose.yaml up -d
```

**DJANGO INIT**
```bash
python src/manage.py createsuperuser
python src/manage.py makemigrations
python src/manage.py migrate
python src/manage.py runserver
```
