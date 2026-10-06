from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Count, Min, Max, Avg, Sum
from django.db.models import F, Value, ExpressionWrapper, DecimalField, Func
from django.db.models.functions import Concat, Length, Lower, Upper, Trim, Replace, Substr, Round, Cast
from tags.models import TaggedItem, ContentType
from django.db import transaction
from store.models import Order, OrderItem, Customer, Product
from django.db import connection

def say_hello(request):
    query_set = Product.objects.all()
    for product in query_set:
        print(product)

#query_set = Product.objects.filter(last_updated__year=2023) #filtering the data based on the year of last updated

   # for product in query_set:
#
#pruduct = Product.object.get(pk=1) picks the actual object usibg the pk(primary key, django automatically chooses the 
#code or id related to the primary key)
#Product = Product.objects.aggregate(Count=Count('id'), Min=Min('price'), Max=Max('price'), Avg=Avg('price'), Sum=Sum('price'))
        '''tittle="My Product",
        slug="my-product",
        description="This is my product",
        price=10.99,
        inventory=100,
        collection_id=1
    )'''
#ExpressionWrapper is used to wrap an expression and specify the output field type. In this case, we are calculating the discounted price by multiplying the price by 0.8 (20% discount) and specifying that the output should be a DecimalField with a maximum of 7 digits and 2 decimal places.
#def say_hello(request):
   # discounted_price = ExpressionWrapper(F('price') * 0.8, output_field=DecimalField(max_digits=7, decimal_places=2))
   # query_set = Product.objects.annotate(discounted_price=discounted_price)
    #for product in query_set:
     #   print(product.tittle, product.price, product.discounted_price)  
    
    #here we can pull data from the database and pass it to the template
    #send email, send a text message, etc
    #return HttpResponse("Hello World")
#CONCATENATION OF STRINGS
    #return HttpResponse("<h1>Hello World</h1>")
   # full_name = Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')


    return render(request, "playground/hello.html")
# Create your views here.
#request handler

def say_hello(request):
    TaggedItem.objects.get_tags_for(Product, 'Sports')
    content_type = ContentType.objects.get_for_model(Product)
    query_set = TaggedItem.objects.filter(content_type=content_type, tag__label='Sports')
    for item in query_set:
        print(item.content_object)


def say_hello(request):
    collection = collection(title="Video Games",
                            featured_product=Product(pk=1))
    collection.save()#method to save the collection object to the database
    Collection = collection.objects.create(title="Video Games", featured_product=Product(pk=1))#method to create a new collection object and save it to the database in one step
    Collection = collection.objects.filter(featured_product__isnull=True)#method to filter the collection objects based on the featured_product field being null
    Collection.update(featured_product=Product(pk=1))#method to update the featured_product field of the collection objects that match the filter criteria
    Collection.objects.update_or_create(title="Video Games", defaults={"featured_product": Product(pk=1)})#method to update an existing collection object with the specified title or create a new one if it doesn't exist, setting the featured_product field to the specified value
    collection.delete()#method to delete the collection object from the database


@transaction.atomic#Wraps the function in a database transaction, ensuring that all database operations within the function are treated as a single unit of work. If any operation fails, the entire transaction is rolled back, maintaining data integrity.
#@transaction.atomic
def say_hello(request):

    order = Order()
    order.customer_id = 1
    order.save()

    item = OrderItem()
    item.order = order
    item.product_id = 1
    item.quantity = 1
    item.unit_price = Product.objects.get(pk=1).price
    item.save()

def say_hello(request):
    query_set = Product.objects.raw("SELECT * FROM store_product").all()
    return render(request, "playground/hello.html")

def say_hello(request):
    with connection.cursor() as cursor:#creates a database cursor that allows you to execute raw SQL queries directly against the database. The connection.cursor() method is used to obtain a cursor object that can be used to execute SQL statements.
        cursor.execute("SELECT * FROM store_product")
        query_set = cursor.fetchall()
    return render(request, "playground/hello.html") 