from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .permissions import IsAdministrator
from .models import Product, Collection, models
from .serializers import ProductSerializer, CollectionSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('collection').all()#All products are retrieved along with their related collection data using select_related for optimization
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]#Athentication required to access the product viewset
    #class definition to access the product viewset and print the current user and authentication status
    def list(self, request, *args, **kwargs):
        print("Current user:", request.user)
        print("Authenticated:", request.user.is_authenticated)#to theck whether user
        return super().list(request, *args, **kwargs)
        #queryset = self.get_queryset()
        #serializer = self.get_serializer(queryset, many=True)
        #return Response(serializer.data)

    def get_queryset(self):
        return Product.objects.select_related('collection').filter(
            owner=self.request.user
        )
     #   owner=self.request.user

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)    
    

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=models.Count('product')
    ).all()
    serializer_class = CollectionSerializer


class ProductList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.select_related('collection').filter(
            owner=request.user#user is authenticated and only products owned by the user are returned
        )

        serializer = ProductSerializer(
            products,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ProductDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id, user):
        return get_object_or_404(
            Product,
            pk=id,
            owner=user
        )

    def get(self, request, id):
        product = self.get_object(id, request.user)

        serializer = ProductSerializer(
            product,
            context={"request": request}
        )

        return Response(serializer.data)#data of the product is returned in the response

    def put(self, request, id):
        product = self.get_object(id, request.user)

        serializer = ProductSerializer(
            product,
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, id):
        product = self.get_object(id, request.user)
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET", "POST"])
def product_list(request):
    if request.method == 'GET':

        products = Product.objects.all()

        serializer = ProductSerializer(
            products,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)

    elif request.method == 'POST':

        serializer = ProductSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(["GET", "POST", "DELETE"])#API view to handle GET, POST, and DELETE requests for product details
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == 'GET':

        serializer = ProductSerializer(
            product,
            context={"request": request}
        )

        return Response(serializer.data)

    elif request.method == 'POST':

        serializer = ProductSerializer(
            product,
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    elif request.method == 'DELETE':

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(
        products_count=models.Count('product')
    ).all()

    serializer_class = CollectionSerializer


# Designing the API for collections
@api_view(["GET", "POST", "DELETE"])
def collection_list(request):

    if request.method == 'GET':

        collections = Collection.objects.annotate(
            products_count=models.Count('product')
        ).all()

        serializer = CollectionSerializer(
            collections,
            many=True
        )

        return Response(serializer.data)

    elif request.method == 'POST':

        serializer = CollectionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    elif request.method == 'DELETE':

        Collection.objects.all().delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


def validate(self, data):
    if data['password'] != data['password_confirmation']:
        return serializers.ValidationError(
            "Password and password confirmation do not match."
        )

    return data


@api_view()
def collection_list(request, id):
    return Response('ok')


@api_view(["GET"])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)

    serializer = CollectionSerializer(
        collection,
        context={"request": request}
    )

    return Response(serializer.data)

#"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzkwNjk1MDY2LCJpYXQiOjE3OTA2OTQ3NjYsImp0aSI6IjcwZjExMGFmOTIyNjRhMDc5MDhmOWVmYWU3ZGU2MGEyIiwidXNlcl9pZCI6IjIifQ.S3EWr9gX_TNNAVtJOMoOS8smD1SrY2K90w9x3kw8q9A"



class AdminProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdministrator]