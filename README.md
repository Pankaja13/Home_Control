#### Project Init

`python3 -m venv venv`

`source venv/bin/activate`

` pip install wheel`

` pip install -r requirements.txt`

`deactivate`

Create `Home_Control\my_settings.py`
```python
THIS_SECRET_KEY = ''
DEBUG = True
ALLOWED_HOSTS = []
```

`python3 manage.py migrate`

`python manage.py collectstatic`

Setup web server/uwsgi or run 
`python manage.py runserver`

#### Create Cron Jobs
`crontab -e -u <username>`
```bash
* * * * * cd /<dir>/Home_Control/ && venv/bin/python3 manage.py runcrons --silent
```