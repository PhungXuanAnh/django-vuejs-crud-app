
# -*- coding: utf-8 -*-
import logging
import pika
import json
import string
import random
import sys
import dateutil.parser
import os

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Product 
from .serializers import * 

logger = logging.getLogger('app')

# @csrf_exempt
@csrf_protect
@api_view(['GET', 'POST'])
def message_handler(request):
    # data=request.data
    # logger.error(data)
    # return Response({}, status=status.HTTP_201_CREATED)

    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
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
        # serializer = ProductSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        data = map_data(data)
        logger.info(json.dumps(data, indent=4, sort_keys=True))
        send_message(data)
        return Response({}, status=status.HTTP_201_CREATED)

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

def map_data(input_data):

    {
    "channel": "mail",
    "datetimeExpire": "2018-06-06T04:25:23.779Z",
    "datetimeSendMessage": "2018-06-06T04:25:21.184Z",
    "templateName": "1",
    "templateParams": "1",
    "users": "1"
    }

    output_data = {
        "id": random_string(32, 2),
        "template": {
            "name": input_data["templateName"],
            "params": input_data["templateParams"]
            # "params": {
            #     "subject": "Email from sigma sender service",
            #     "from_email": "sender@sigma.com",
            #     "var1": "value of var1",
            #     "var2": "value of var2",
            # }
        },
        "channel": input_data["channel"],
        "users": [] + input_data["users"].split(' '),
        # "send_time": "now",
        "send_time": dateutil.parser.parse(input_data["datetimeSendMessage"]).strftime("%Y-%m-%d %H:%M:%S"), # "2018-05-21 03:40:00",
        "expires": dateutil.parser.parse(input_data["datetimeExpire"]).strftime("%Y-%m-%d %H:%M:%S"), # "2019-05-21 03:40:00",
    }

    return output_data


def random_string(n=10, random_type=0, prefix=''):
    """
    Generate random string

    :param n: number character
    :param random_type: type of random string: 1- digits, 2 - ascii lowercase + digits,  3 - ascii uppercase + digits
    :param prefix: prefix of random string
    :return: string
    """
    letters = string.ascii_letters + string.digits
    if random_type == 1:
        letters = string.digits
    elif random_type == 2:
        letters = string.ascii_lowercase + string.digits
    elif random_type == 3:
        letters = string.ascii_uppercase + string.digits

    result = prefix + ''.join(random.choice(letters) for _ in range(n))

    return result

def send_message(dict_msg):
    env = os.getenv
    RABBITMQ_HOST = env('RABBITMQ_HOST', '127.0.0.1')
    RABBITMQ_PORT = env('RABBITMQ_PORT', '5672')
    RABBITMQ_QUEUE = '{}_channel'.format(dict_msg["channel"])

    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

    # Send message
    channel.basic_publish(exchange='',
                        routing_key=RABBITMQ_QUEUE,
                        body=json.dumps(dict_msg),
                        properties=pika.BasicProperties(
                            delivery_mode=2,  # make message persistent
                        ))

    # logger.info("[x] Sent message to: {}".format(RABBITMQ_HOST))
    connection.close()
    

if __name__ == '__main__':
    data = {
        "id": random_string(32, 2),
        "template": {
            "name": "templates.template",
            "params": {
                "subject": "Email from sigma sender service",
                "from_email": "sender@sigma.com",
                "var1": "value of var1",
                "var2": "value of var2"
            }
        },
        "channel": "mail",
        "users": ['phungxuananh1991@gmail.com'],
        # "send_time": "now",
        "send_time": "2018-05-21 03:40:00",
        "expires": "2019-05-21 03:40:00",
    }

    send_message(data)
