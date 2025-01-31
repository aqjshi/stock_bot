\documentclass[11pt]{article}

% Packages for links, code listings, and better formatting
\usepackage[hidelinks]{hyperref}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{enumitem}
\usepackage{geometry}
\geometry{margin=1in}

% Code listing settings
\lstset{
    basicstyle=\ttfamily\footnotesize,
    breaklines=true,
    frame=single,
    columns=fullflexible,
}

\title{Stock Trading Bot Documentation}
\author{Anthony \& Hailey}
\date{\today}

\begin{document}

\maketitle

\section{Tech Stack}
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Python 3.12} --- \url{https://github.com/python}
    \item \textbf{Django} --- \url{https://github.com/django/django} \quad (\texttt{pip install "Django>=5.1,<5.2"})
    \item \textbf{TimescaleDB Cloud} --- \url{https://tsdb.co/justin} (or Docker version)
    \item \textbf{Django Timescaledb} --- \url{https://github.com/jamessewell/django-timescaledb} \quad (\texttt{pip install django-timescaledb})
    \item \textbf{Python requests} --- \url{https://github.com/psf/requests} \quad (\texttt{pip install requests})
    \item \textbf{Jupyter} --- \url{https://jupyter.org/} \quad (\texttt{pip install jupyter})
    \item \textbf{Psycopg Binary Release} --- \url{https://pypi.org/project/psycopg/} \quad (\texttt{pip install "psycopg[binary]"})
    \item \textbf{Python Decouple} --- to load environment variables (e.g., \texttt{.env}) with type casting and default values.
    \item \textbf{Polygon.io} --- \url{https://polygon.io/?utm_source=cfe&utm_medium=github&utm_campaign=cfe-github} \quad [\textit{docs:} \url{https://polygon.io/docs/stocks/getting-started?utm_source=cfe&utm_medium=github&utm_campaign=cfe-github}]
    \item \textbf{Alpha Vantage} --- \url{https://www.alphavantage.co/?utm_source=cfe&utm_medium=github&utm_campaign=cfe-github} \quad [\textit{docs:} \url{https://www.alphavantage.co/documentation/?utm_source=cfe&utm_medium=github&utm_campaign=cfe-github}]
    \item \textbf{OpenAI} --- \url{https://www.openai.com/?utm_source=cfe&utm_medium=github&utm_campaign=cfe-github}
\end{itemize}

\section{Tutorial}
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{In-depth Setup:} \url{https://youtu.be/aApDye1TWJ4}
    \item \textbf{Django Setup in Jupyter Notebooks (short + code):} \url{https://www.codingforentrepreneurs.com/shorts/django-setup-for-use-in-jupyter-notebooks}
    \item \textbf{Full Tutorial:} \url{https://youtu.be/O3O1z5hTdUM}
\end{itemize}

\section{Getting Started}
\subsection*{Required Downloads}
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Git} --- \url{https://git-scm.com/}
    \item \textbf{VSCode} --- \url{https://code.visualstudio.com/} (or \textbf{Cursor} --- \url{https://cursor.com/})
    \item \textbf{Docker Desktop} --- \url{https://www.docker.com/products/docker-desktop/} or Docker Engine via \url{https://get.docker.com/}
    \item \textbf{Python} --- \url{https://www.python.org/downloads/}
\end{itemize}

\subsection*{Accomplishments}
\begin{itemize}[leftmargin=1.2cm]
    \item POLYGON API integration
    \item Generation of complete dataset
    \item Working local data structure and SQLite queries
\end{itemize}

\section{API Services}
\begin{verbatim}
ALPHA_VANTAGE_API_KEY="CSZDVN7BYPHHRPF4"
\end{verbatim}

\section{To Do}
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Hailey:}
    \begin{itemize}
        \item Integrate ALPHA VANTAGE API
        \item Checkout new branch and review Alpha Vantage API documentation
        \item Open Docker Desktop and run \texttt{docker compose up -d}
        \item Run \texttt{src/manage.py createsuperuser} (if not already created)
        \item Run \texttt{src/manage.py runserver} and log in using the provided URL
        \item Data is stored in \texttt{src/db.sqlite3}; see \texttt{bulk_load.ipynb} (approx.\ 20--80 MB depending on OS)
        \item Create a testing environment in Jupyter (see \texttt{alpha_vantage_bulk_load.ipynb})
        \item Adapt Polygon subfunctions to Alpha Vantage equivalents and integrate into \texttt{alpha_vantage.py}
        \item Verify URL functionality, create new variables for each technical indicator (format: \texttt{alpha_vantage\_\<indicator\>})
        \item Run migrations and check updates via the Django admin interface
        \item Upon completion of \texttt{alpha_vantage\_bulk\_load.ipynb}, \texttt{alpha_vantage.py}, and \texttt{src/market/models.py}, finalize and deliver
    \end{itemize}
    \item \textbf{Anthony:}
    \begin{itemize}
        \item \textbf{Part 1:}
        \begin{itemize}
            \item Create train/validation/test sets (sections 1 \& 2)
            \item Implement the model and evaluate performance
        \end{itemize}
        \item \textbf{Part 2:}
        \begin{itemize}
            \item Mine for optimal window size (\(k\)) for data
            \item Evaluate using the Sharpe ratio
        \end{itemize}
    \end{itemize}
\end{itemize}

\section{Additional Instructions}
\subsection*{Convert Markdown Text to a Jupyter Notebook}
Use Jupytext:
\begin{lstlisting}[language=bash]
jupytext --to notebook nbs/build_dataset.py
\end{lstlisting}

\subsection*{Clone the Repository}
Open a terminal and run:
\begin{lstlisting}[language=bash]
git clone https://github.com/aqjshi/stock_bot.git
\end{lstlisting}

\subsection*{Initialize Your Environment}
\begin{enumerate}[label=\arabic*.]
    \item Create your \texttt{.env} file:
    \begin{lstlisting}[language=bash]
touch .env
    \end{lstlisting}
    \item Checkout the \texttt{start} branch and reinitialize Git:
    \begin{lstlisting}[language=bash]
git checkout start
rm -rf .git
git init
git add --all
git commit -m "It's my bot now"
    \end{lstlisting}
    \item Create a Python virtual environment:
    \begin{itemize}
        \item \textbf{macOS/Linux/WSL:}
        \begin{lstlisting}[language=bash]
python3.12 -m venv venv
source venv/bin/activate
        \end{lstlisting}
        \item \textbf{Windows (PowerShell):}
        \begin{lstlisting}[language=powershell]
c:\Path\To\Python312\python.exe -m venv venv
.\venv\Scripts\activate
        \end{lstlisting}
    \end{itemize}
    \item Install requirements:
    \begin{lstlisting}[language=bash]
(venv) python -m pip install -r requirements.txt
    \end{lstlisting}
\end{enumerate}

\subsection*{Docker Compose (Local TimescaleDB and Redis)}
\begin{lstlisting}[language=bash]
docker compose -f compose.yaml up -d
\end{lstlisting}

\subsection*{Django Initialization}
\begin{lstlisting}[language=bash]
python src/manage.py createsuperuser
python src/manage.py makemigrations
python src/manage.py migrate
python src/manage.py runserver
\end{lstlisting}

\end{document}
