from rest_framework import generics, viewsets
from .models import MenuItem, Category, Cart, Order, OrderItem, User
from .serializers import MenuItemSerializer, CategorySerializer, UserSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .throttles import TenCallsPerMinute
from django.contrib.auth.models import User, Group


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    search_fields = ['category__title']

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.all().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        Cart.objects.all().filter(user=self.request.user).delete()
        return Response("Cart cleared", status=status.HTTP_200_OK)


class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        elif self.request.user.groups.count() == 0:
            return Order.objects.all().filter(user=self.request.user)
        elif self.request.user.groups.filter(name='Delivery Crew').exists():
            return Order.objects.all().filter(delivery_crew=self.request.user)
        else:
            return Order.objects.all()

    def create(self, request, *args, **kwargs):
        menuitem_count = Cart.objects.all().filter(user=self.request.user).count()
        if menuitem_count == 0:
            return Response("Cart is empty", status=status.HTTP_400_BAD_REQUEST)
        data = request.data.copy()
        total = self.get_total_price(self.request.user)
        data['total'] = total
        data['user'] = self.request.user.id
        order_serializer = OrderSerializer(data=data)
        if order_serializer.is_valid():
            order = order_serializer.save()
            items = Cart.objects.all().filter(user=self.request.user).all()

            for item in items.values():
                order_item = OrderItem(
                    order=order,
                    menu_item_id=item['menuitem_id'],
                    quantity=item['quantity']
                )
                order_item.save()

            Cart.objects.all().filter(user=self.request.user).delete()

            result = order_serializer.data.copy()
            result['total'] = total
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)

    def get_total_price(self, user):
        total = 0
        items = Cart.objects.all().filter(user=user).all()
        for item in items.values():
            total += item['price']
        return total


class SingleOrderView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if self.request.user.groups.count() == 0:
            return Response("You are not a delivery crew", status=status.HTTP_400_BAD_REQUEST)
        else:
            return super().update(request, *args, **kwargs)


class GroupViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    def list(self, request):
        users = User.objects.all().filter(groups__name='Manager')
        items = UserSerializer(users, many=True)
        return Response(items.data)

    def create(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        managers = Group.objects.get(name='Manager')
        managers.user_set.add(user)
        return Response("User is now a manager", status=status.HTTP_200_OK)

    def destroy(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        managers = Group.objects.get(name='Manager')
        managers.user_set.remove(user)
        return Response("User is no longer a manager", status=status.HTTP_200_OK)


class DeliveryCrewViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        users = User.objects.all().filter(groups__name='Delivery Crew')
        items = UserSerializer(users, many=True)
        return Response(items.data)

    def create(self, request):
        if self.request.user.is_superuser == False:
            if self.request.user.groups.filter(name='Manager').exists() == False:
                return Response("You are not a manager", status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, username=request.data['username'])
        dc = Group.objects.get(name='Delivery Crew')
        dc.user_set.add(user)
        return Response("User is now from the delivery crew", status=status.HTTP_200_OK)

    def destroy(self, request):
        if self.request.user.is_superuser == False:
            if self.request.user.groups.filter(name='Manager').exists() == False:
                return Response("You are not a manager", status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, username=request.data['username'])
        dc = Group.objects.get(name='Delivery Crew')
        dc.user_set.remove(user)
        return Response("User is no longer from the delivery crew", status=status.HTTP_200_OK)


@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message": "Successful."})


@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def throttle_check_auth(request):
    return Response({"message": "Only logged in users can see this."})


@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message": "Some secret message"})

# @api_view(['GET', 'POST'])
# def menu_items(request):
#     if (request.method == 'GET'):
#         items = MenuItem.objects.select_related('category').all()
#         category_name = request.query_params.get('category')
#         to_price = request.query_params.get('to_price')
#         search = request.query_params.get('search')
#         ordering = request.query_params.get('ordering')
#         perpage = request.query_params.get('perpage', default=2)
#         page = request.query_params.get('page', default=1)
#         if category_name:
#             items = items.filter(category__title__iexact=category_name)
#         if to_price:
#             items = items.filter(price__lte=to_price)
#         if search:
#             items = items.filter(title__istartswith=search)
#         if ordering:
#             ordering_fields = ordering.split(",")
#             items = items.order_by(*ordering_fields)
#         paginator = Paginator(items, per_page=perpage)
#         try:
#             items = paginator.page(number=page)
#         except EmptyPage:
#             items = []
#         serialized_item = MenuItemSerializer(items, many=True)
#         return Response(serialized_item.data)
#     if (request.method == 'POST'):
#         serialized_item = MenuItemSerializer(data=request.data)
#         serialized_item.is_valid(raise_exception=True)
#         # serialized_item._validated_data     # Accessing validated data
#         serialized_item.save()  # Save the record in the database
#         # Access the method after saving it (You can't without save!)
#         return Response(serialized_item.data, status.HTTP_201_CREATED)


# @api_view()
# def single_item(request, id):
#     item = get_object_or_404(MenuItem, pk=id)
#     serialized_item = MenuItemSerializer(item)
#     return Response(serialized_item.data)


# @api_view(['GET', 'POST'])
# def categories(request):
#     if request.method == 'GET':
#         items = Category.objects.all()
#         serialized_item = CategorySerializer(items, many=True)
#         return Response(serialized_item.data)
#     if request.method == 'POST':
#         serialized_item = CategorySerializer(data=request.data)
#         serialized_item.is_valid(raise_exception=True)
#         # serialized_item._validated_data     # Accessing validated data
#         serialized_item.save()  # Save the record in the database
#         # Access the method after saving it (You can't without save!)
#         return Response(serialized_item.data, status.HTTP_201_CREATED)


# @api_view()
# def single_category(request, id):
#     item = get_object_or_404(Category, pk=id)
#     serialized_item = CategorySerializer(item)
#     return Response(serialized_item.data)


# @api_view()
# @permission_classes([IsAuthenticated])
# def manager_view(request):
#     if request.user.groups.filter(name='Manager').exists():
#         return Response({"message": "Only Manager should see this!"})
#     else:
#         return Response({"message": "You are not authorized."}, 403)


# @api_view(['POST'])
# @permission_classes([IsAdminUser])
# def managers(request):
#     username = request.data['username']
#     if username:
#         user = get_object_or_404(User, username=username)
#         managers = Group.objects.get(name='Manager')
#         if request.method == 'POST':
#             managers.user_set.add(user)
#             return Response({"message": "User added as manager."})
#         if request.method == 'DELETE':
#             managers.user_set.remove(user)
#             return Response({"message": "User is not a manager anymore."})
#     return Response({"message": "error"}, status.HTTP_400_BAD_REQUEST)
