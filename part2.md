## Building the REST API

Django REST framework is a powerful and easy to use package for building Web APIs.

Let's get started by building a simple REST API using Django REST framework.

### Adding the Product Model

Django has a powerful ORM (Object Relational Mapper) that allows you to work with multiple database management systems without actually writing any SQL. All you need to do is to define models in Python classes and Django will take care of mapping Python classes to SQL queries.

The API is built around a simple product model so continuing with the project you've built in the previous part open the **catalog/models.py** file then add the following model

```python
from django.db import models

class Product(models.Model):

    sku = models.CharField(max_length=13,help_text="Enter Stock Keeping Unit")    
    name = models.CharField(max_length=200, help_text="Enter product name")
    description = models.TextField(help_text="Enter product description")

    buyPrice = models.DecimalField(decimal_places=2, max_digits=20,help_text="Enter product price per unit")
    sellPrice = models.DecimalField(decimal_places=2, max_digits=20,help_text="Enter product price per unit")

    unit = models.CharField(max_length=10,help_text="Enter product unit")

    quantity = models.DecimalField(decimal_places=1, max_digits=20,help_text="Enter quantity")

    def get_absolute_url(self):
         """
         Returns the url to access a particular instance of Product.
         """
         return reverse('product-detail-view', args=[str(self.id)])

    def __str__(self):

        return self.sku
```

Now you need to migrate your database to add the new changes

```shell
python manage.py makemigrations
python manage.py migrate
```

Next let's add some seed data using a data migration

So first make an empty migration by running the following command:

```shell
python manage.py makemigrations catalog --empty

```

Next open your migration file in your app migrations folder (**catalog/migrations**) then create a function that will executed by the **RunPython()** method when you apply your migration

```python
from django.db import migrations
from django.conf import settings

def create_data(apps, schema_editor):
    Product = apps.get_model('catalog', 'Product')
    Product(sku='sku1',name='Product 1', description='Product 1', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=100).save()
    Product(sku='sku2',name='Product 2', description='Product 2', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=200).save()
    Product(sku='sku3',name='Product 3', description='Product 3', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=300).save()

    Product(sku='sku4',name='Product 4', description='Product 1', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=100).save()
    Product(sku='sku5',name='Product 5', description='Product 2', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=200).save()
    Product(sku='sku6',name='Product 6', description='Product 3', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=300).save()
    Product(sku='sku7',name='Product 7', description='Product 4', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=400).save()

    Product(sku='sku8',name='Product 8', description='Product 1', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=100).save()
    Product(sku='sku9',name='Product 9', description='Product 2', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=200).save()
    Product(sku='sku10',name='Product 10', description='Product 3', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=300).save()
    Product(sku='sku11',name='Product 11', description='Product 4', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=400).save()

    Product(sku='sku12',name='Product 12', description='Product 1', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=100).save()
    Product(sku='sku13',name='Product 13', description='Product 2', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=200).save()
    Product(sku='sku14',name='Product 14', description='Product 3', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=300).save()
    Product(sku='sku15',name='Product 15', description='Product 4', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=400).save()

    Product(sku='sku16',name='Product 16', description='Product 1', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=100).save()
    Product(sku='sku17',name='Product 17', description='Product 2', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=200).save()
    Product(sku='sku18',name='Product 18', description='Product 3', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=300).save()
    Product(sku='sku19',name='Product 19', description='Product 4', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=400).save()

    Product(sku='sku20',name='Product 20', description='Product 1', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=100).save()
    Product(sku='sku21',name='Product 21', description='Product 2', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=200).save()
    Product(sku='sku22',name='Product 22', description='Product 3', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=300).save()
    Product(sku='sku23',name='Product 23', description='Product 4', buyPrice=100 , sellPrice=100,unit='kilogram', quantity=400).save()

class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_data),
    ]
```

You can then migrate your database to create the initial data

```shell
python manage.py migrate
```

### Adding the Serializer Class

From [Django REST framework docs](http://www.django-rest-framework.org/api-guide/serializers/) here is the definition of a serializer

    Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into JSON, XML or other content types. Serializers also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the incoming data.

Create a **serializers.py** file inside your the catalog app folder then add the following code to create a serializer class for the product model

```python
from rest_framework import serializers
from .models import Product
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product 
        fields = ('pk','sku', 'name', 'description', 'buyPrice','sellPrice','unit','quantity')
```

### Adding the API Views

After adding the database model and the serializer class and also some seed data the next thing is to create the API views that will be responsible for creating, updating, deleting and fetching data from the database and send it back to users as JSON database when users request the appropriate API endpoint so go ahead and open the **catalog/views.py** file then start by adding the following imports

```python
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product
from .serializers import *
```

This code imports different classes from DRF package, paginator classes to add pagination and then the Product model and its serializer class.

### Adding the Product List/Create API View

In your **catalog/views.py** add the following view function which can process either GET or POST requests to either return paginated list of products or create a product.

```python
@api_view(['GET', 'POST'])
def product_list(request):
    """
    List  products, or create a new product.
    """
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        products = Product.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(products, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = ProductSerializer(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/products/?page=' + str(nextPage), 'prevlink': '/api/products/?page=' + str(previousPage)})

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

This function first checks if it's a GET or POST request then preforms the processing based on the type of the request:

- If it's a GET request, the function retrieves the page number from the GET request or use the first page by default if no page is submitted then retrieves the request page of products, serialize it and return it back alongside with other information such as the next page and previous page links.
- If it's a POST request, the function creates the product based on the POST data.

### Adding the Product Detail API View

Now you need to add the view function that will be responsible for getting, updating or deleting a single product by id depending on the type of the HTTP request (GET, PUT or DELETE).

```python
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    """
    Retrieve, update or delete a product instance.
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

This view method first checks if a product, with the primary key passed as a parameter, exists. If it does exist it returns a 404 response otherwise it checks for the request method:

- If it's a GET the product is simply returned
- If it's a PUT the product is updated
- If it's a DELETE the product is deleted

### Adding API Endpoints

Next you need to create the two API endpoints **api/products/** for querying and creating products **and api/products/<id>** for displaying single product information, updating and deleting single products by their id.

Go ahead and open **backend/urls.py** then add

```python
##...
from catalog import views
##...

urlpatterns = [
    ##...
    url(r'^api/products/$', views.product_list),
    url(r'^api/products/(?P<pk>[0-9]+)$', views.product_detail),
    ##...

]
```
Re-run django server

```shell
python manage.py runserver
```

## Creating the Service to Consume the API

Now that you have created the API you need to consume it from your app front-end built with Vue. You'll use the Axios HTTP client to make HTTP calls to the API.

For the sake of organizing the code you'll encapsulate all the code that communicates with the API in one single class that will be used from different views to make any calls to the API endpoints.

So inside **frontend/src** create an http folder (or call it whatever you want) then create the **APIService.js** class

This class provides wrapper methods for the Axios get, post, put and delete methods.

The APIService.js class contains these methods

- getProducts(): you'll use this method to retrieve paginated list of products
- getProduct(pk): you'll use this method to retrieve a product by id/primary key
- createProduct(product): you'll use this method to create a product
- updateProduct(product): you'll use this method to update a product
- deleteProduct(product): you'll use this method to delete a product

In **APIService.js** copy the following code
