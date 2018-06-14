# Easy to develop

create 2 file in **catalog/templates/** name **index_prod.html** and **index_dev.html**

add to **index_prod.html**:

```html

{% load render_bundle from webpack_loader %}

<html  lang="en">
<head>
<meta  charset="UTF-8">
<title>Django - Auth0 - Vue</title>
{% render_bundle 'app' 'css' %}

</head>
<body>
<div  id=app>
</div>

{% render_bundle 'manifest' %}
{% render_bundle 'vendor' %}
{% render_bundle 'app' 'js' %}
</body>
</html>

```

add to **index_dev.html**:

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

change **`settings.py`**:

```python

IS_PRODUCTION = True

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': '',
        'STATS_FILE': os.path.join(BASE_DIR, '../webpack-stats-prod.json' if IS_PRODUCTION else '../webpack-stats.json'),
    }
}

CATALOG_TEMPLATE = 'index_prod.html' if IS_PRODUCTION else 'index_dev.html'

```

Add and change **views.py**:

```python

//...
from django.conf import settings

//...

urlpatterns = [
    url(r'^api/products/$', views.product_list),
    url(r'^api/products/(?P<pk>[0-9]+)$', views.product_detail),
    url(r'^(?:.*)/?$', TemplateView.as_view(template_name=settings.CATALOG_TEMPLATE), name='catchall'),
    path('admin/', admin.site.urls),
]

```