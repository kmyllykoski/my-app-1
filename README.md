# Django app for uploading and processing pdf-files

##(On Windows) Install UV (https://docs.astral.sh/uv/getting-started/installation/#installation-methods)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

##Install dependencies
uv pip install

##Activate the virtual environment
.venv\Scripts\activate

##Run Django server
uv run python manage.py runserver
