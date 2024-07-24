#! /bin/bash

# installng poetry and creating poetry venv
cd /app && poetry install

# run python program to start streamlit app
poetry run streamlit run /app/streamlit.py