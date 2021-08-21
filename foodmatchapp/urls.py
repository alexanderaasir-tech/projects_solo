from django.urls import path
from . import views
urlpatterns = [
    path('',views.index),
    path('users/create', views.create_user),
    path('dashboard', views.dashboard),
    path('users/login', views.login),
    path('logout', views.logout),

    path('restaurant/new', views.new_restaurant),
    path('restaurant/create', views.create_restaurant),
    path('restaurant/remove/<int:restaurant_id>', views.delete_restaurant),

    path('item/new/<int:restaurant_id>', views.new_item),
    path('item/create/<int:restaurant_id>', views.create_item),
    
    path('restaurant/menu/<int:restaurant_id>', views.order_items),

    #adding item to a user order to be displayed on the dashboard
    path('add_items',views.add_items),
]