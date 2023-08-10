from django.urls import path
from .views import login_user,logout_user,return_hello
from . import views

# Import the handler_404 function
# from .views import handler_404

# TODO : 404
# handler_404 = 'web.views.handler_404'
 
urlpatterns = [
    path('index', views.index, name='index'),
    path('list_and_display/', views.list_and_display_tables, name='list_and_display_tables'),
    path('display/<str:table_name>/', views.display_table, name='display_table'),
    path('',views.login_user,name="login_user"),
    path('logout_user',views.logout_user,name="logout_user"),
    
    # Use the handler_404 function as a callable
    # path('<str:path>/', handler_404),
]

