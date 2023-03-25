# Django IFRC API

This repo specifies the backend, and consquently the API for the IFRC Community Sampling Tool. The frontend of the tool can be found in [ifrc-sampling](https://github.com/hubamatyas/ifrc-sampling).

## Deployment Mannual

### Configure virtual environment

Run `python -m venv .venv` to create a virtual environmet.

Run `source ./.venv/bin/activate` to activate the virtual environment.

### Install requirements

Run `pip install -r requirements.txt` to install dependecies

Add database password as an environment variable with
- `export DB_PASSWORD=YOUR_PASSWORD` on Mac or Linux
- `set DB_PASSWORD=YOUR_PASSWORD` on Windows

### Run the REST API locally on port 8000

Run `python manage.py runserver`

Test it by copying `http://127.0.0.1:8000/api/decision-tree/1` into the searchbar.

## API Documentation

- See API Documentation [here](./sampling/README.md)
