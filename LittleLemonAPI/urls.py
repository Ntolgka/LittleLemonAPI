from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # path('menu-items/', views.MenuItemsView.as_view()),
    # path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    # path('category', views.CategoriesView.as_view()),
    # path('category/<int:pk>', views.SingleCategoryView.as_view()),
    # path('menu-items/', views.menu_items),
    # path('menu-items/<int:id>', views.single_item),
    # path('category/', views.categories),
    # path('category/<int:id>', views.single_category),
    # path('manager-view/', views.manager_view),
    # path('groups/manager/users/', views.managers),

    path('categories/', views.CategoriesView.as_view()),
    path('menu-items/', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('cart/menu-items/', views.CartView.as_view()),
    path('orders/', views.OrderView.as_view()),
    path('orders/<int:pk>', views.SingleOrderView.as_view()),
    path('groups/manager/users/', views.GroupViewSet.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'})),
    path('groups/delivery-crew/users/', views.DeliveryCrewViewSet.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'})),
    path('api-token-auth/', obtain_auth_token),
    path('throttle-check/', views.throttle_check),
    path('throttle-check-auth/', views.throttle_check_auth),
    path('secret/', views.secret),


]
