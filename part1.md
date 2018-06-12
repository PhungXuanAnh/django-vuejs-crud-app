# Guide step by step

## Create backend and frontend folders

```shell
mkdir backend
mkdir frontend
```

## Bootstrapping the Back-End Project

```shell
cd backend/
virtualenv3 .
source .python3/bin/activate

pip install django
django-admin startproject backend .
python manage.py startapp catalog
python manage.py migrate
python manage.py runserver
```

If you navigate to http://127.0.0.1:8000 in a web browser, you will see the following homepage:


## Bootstrapping the Front-end Project

```shell
cd ../frontend
Sudo npm install -g vue-cli

```