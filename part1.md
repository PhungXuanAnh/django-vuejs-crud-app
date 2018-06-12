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
Sudo npm install -g vue-cli

# initialize Vue.js with the Webpack template
cd ..
vue init webpack frontend

```

Vue.js will ask a bunch of questions while creating your project. You can answer them as follows:


    ? Project name frontend
    ? Project description A Vue.js project
    ? Author Phung Xuan Anh <anhpx@sigma-solutions.eu>
    ? Vue build standalone
    ? Install vue-router? Yes
    ? Use ESLint to lint your code? No
    ? Set up unit tests No
    ? Setup e2e tests with Nightwatch? No
    ? Should we run `npm install` for you after the project has been created? (recommended) npm


```shell
# change working directory to the front-end
cd frontend

# run the NPM dev script
npm run dev
```

After that, you should be able to visit the Vue.js application in your browser by navigating to http://127.0.0.1:8080.


```shell

pip install djangorestframework

```

Next, you'll need to add these packages to the list of installed apps in settings.py

```python
INSTALLED_APPS = [
    #...
    'rest_framework'
]
```

**Enabling CORS on Django**

As you are going to create a Vue.js application to consume the Django endpoints, you will need to enable CORS on your Django project. To do that, you can install the django-cors-headers utility as follows:

```shell
pip install django-cors-headers

```

After that, you have to add this utility to your installed apps in the settings.py file:

```python
INSTALLED_APPS = [
    # ...
    'corsheaders',
]
```

Then, you have to add the CorsMiddleware in this same file:

```python
MIDDLEWARE = [  # Or MIDDLEWARE_CLASSES on Django < 1.10
    # ...
    'corsheaders.middleware.CorsMiddleware'
]
```

The last thing you will need to do is to configure what origins will be accepted in your Django application:

```python
CORS_ORIGIN_WHITELIST = (
    'localhost:8080',
    'localhost:8000',
)
```

You also need to install Axios to send AJAX requests to the Django back-end:

```shell
npm install --save axios
```

