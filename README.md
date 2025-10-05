# Django app for uploading and processing pdf-files

### Clone the repo in your own folder

### (On Windows) Install UV (https://docs.astral.sh/uv/getting-started/installation/#installation-methods)
```powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"```

### Install dependencies
```uv pip install```

### Activate the virtual environment
```.venv\Scripts\activate```

### Run Django server
```uv run python manage.py runserver```

Dokploy deployment 

To do handle migrations add this to environment variables:
```NIXPACKS_START_CMD="python manage.py migrate && python manage.py collectstatic --noinput && gunicorn mysite.wsgi"```
https://www.answeroverflow.com/m/1235078349714493500

Example environment:

DJANGO_DEBUG=False
DJANGO_SECRET_KEY=django-insecure-7$s%f....
DATABASE_URL=postgresql://user:password@instance_name_given_by_dokploy:5432/pdf_data
PORT=8000
NIXPACKS_START_CMD="python manage.py migrate && python manage.py collectstatic --noinput && gunicorn mysite.wsgi"





