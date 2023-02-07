# Django IFRC API

This repo specifies the backend, and consquently the API for the IFRC Community Sampling Tool. The frontend of the tool can be found in [ifrc-sampling](https://github.com/hubamatyas/ifrc-sampling).

## Install requirements

`pip install -r requirements.txt`

### Run the REST API locally on port 8000

`python manage.py runserver`

Test it by copying `http://127.0.0.1:8000/api/decision-tree/2` into the searchbar.
