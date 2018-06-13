
- [Create backend and frontend folders](#create-backend-and-frontend-folders)
- [Bootstrapping the Back-End Project](#bootstrapping-the-back-end-project)
- [Bootstrapping the Front-end Project](#bootstrapping-the-front-end-project)
- [Integrating Vue and Django](#integrating-vue-and-django)
- [Serving the Index Template](#serving-the-index-template)
- [Fixing Hot Code Reloading](#fixing-hot-code-reloading)

## Bootstrapping the Back-End Project

```shell
cd backend/
virtualenv3 .
source .python3/bin/activate

pip install django
django-admin startproject backend
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

## Integrating Vue and Django

Next run the following command to install the Webpack loader package for integrating Webpack with Django


```shell
pip install django-webpack-loader

```

Then go to your project settings.py file and add webpack_loader to INSTALLED_APPS :

```python
INSTALLED_APPS = [
    'webpack_loader'
]
```

Next you need to add the following object to settings.py to configure the Webpack loader

```python
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': '',
        'STATS_FILE': os.path.join(BASE_DIR, '../webpack-stats.json'),
    }
}

```

This tells Webpack loader to look for **webpack-stats.json** in the root folder of the project. This file holds information about the static assets that Webpack has generated (you will see next how to generate this file).

## Serving the Index Template

Now you need to create and serve an **index.html** file, where you can mount the Vue application, using a Django view

First create the **index.html** template in **catalog/templates/index.html** then add the following content.

```html
{% load render_bundle from webpack_loader %}

<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Django - Auth0 - Vue</title>

</head>
<body>
<div id="app">
</div>
{% render_bundle 'app' %}
</body>
</html>

```

The page contains a ** <div> ** with the id app where you can mount the Vue application.

The **render_bundle** tag (with app as an argument) is used to include the app bundle files.

After creating the template, you can next use TemplateView to serve it. Go to your project **urls.py**` file then add the following:

```python
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls import url

from catalog import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    path('admin/', admin.site.urls),
]

```

Now reload your Django application, you will get the Yellow page with an error with Django complaining about not finding the **webpack-stats.json** file needed by the Webpack loader.

    Error reading /xxxx/xxxx/xxxx/django-auth0-vue-part-2/webpack-stats.json. Are you sure webpack has generated the file and the path is correct?

This is a screen shot of the error that you will get

To get rid of this error you need to generate the **webpack-stats.json** file using the Webpack plugin **webpack-bundle-tracker** so first install it from npm using (make sure you are inside the Vue application):

```shell
npm install webpack-bundle-tracker --save

```

In **frontend/build/webpack.dev.conf.js** import **webpack-bundle-tracker** and include **BundleTracker** in Webpack plugins:

```javascript
const BundleTracker = require('webpack-bundle-tracker')
/*...*/

  plugins: [
    /*...*/
    new BundleTracker({filename: '../webpack-stats.json'})
  ]

```

This tells webpack-bundle-tracker to generate the stats file in the root folder of your project.

If you re-run you Webpack dev server, you'll have the webpack-stats.json file generated in root of your project:

If you visit you Django app now you'll get this error in the console

Loading failed for the <script> with source “http://127.0.0.1:8000/app.js”.


You can fix this error by going to **frontend/config/index.js** next locate the **assetsPublicPath** setting and change its value from / to http://localhost:8080/


```javascript
/*...*/
module.exports = {
  dev: {

    // Paths
    assetsSubDirectory: 'static',
    assetsPublicPath: 'http://localhost:8080/',
    proxyTable: {},
    /*...*/
```

Next **re-run** your frontend app:

```shell
npm run dev
or
npm start

```

## Fixing Hot Code Reloading

Now in **frontend/build/webpack.dev.conf.js** you need to configure the Webpack Dev server to accept requests from other origins such as http://localhost:8000 since the Django server will send XHR requests to http://localhost:8080 for getting the source file changes.

Add **frontend/build/webpack.dev.conf.js** a headers object in devServer. 

```javascript

devServer: 
    { 
        /*...*/
        headers: { 'Access-Control-Allow-Origin': '\*' }, 
        /*...*/
    },

```

This will fix Hot Code Reloading when using Django server to serve Vue files. To test that, just change something in your Vue application and you'll be able to see your web page hot reloaded to see the changes without having to manually reload it.

That's all you need to do. Now re-run the Vue dev server then navigate with your browser to http://localhost:8000/. You'll be now able to interact with your application served from the Django dev server.

Next **re-run** your frontend app:

```shell
npm run dev
or
npm start

```

Try to change something in file **frontend/src/components/HelloWorld.vue**, for example change **Welcome to Your Vue.js App** to **Welcome to Your Vue.js App aaaaaaaaaaaaaaaa** and see the change in web


