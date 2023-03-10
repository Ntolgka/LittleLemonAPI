from rest_framework import generics
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status


@api_view(['GET', 'POST'])
def menu_items(request):

    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        serialized_item = MenuItemSerializer(items, many=True)
        return Response(serialized_item.data)

    if request.method == 'POST':
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        # serialized_item._validated_data     # Accessing validated data
        serialized_item.save()  # Save the record in the database

        # Access the method after saving it (You can't without save!)
        return Response(serialized_item.data, status.HTTP_201_CREATED)


@api_view()
def single_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)


@api_view(['GET', 'POST'])
def categories(request):

    if request.method == 'GET':
        items = Category.objects.all()
        serialized_item = CategorySerializer(items, many=True)
        return Response(serialized_item.data)

    if request.method == 'POST':
        serialized_item = CategorySerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        # serialized_item._validated_data     # Accessing validated data
        serialized_item.save()  # Save the record in the database

        # Access the method after saving it (You can't without save!)
        return Response(serialized_item.data, status.HTTP_201_CREATED)


@api_view()
def single_category(request, id):
    item = get_object_or_404(Category, pk=id)
    serialized_item = CategorySerializer(item)
    return Response(serialized_item.data)


# class MenuItemsView(generics.ListCreateAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer
# class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer
