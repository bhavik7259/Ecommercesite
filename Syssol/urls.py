from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import SearchResultsView



urlpatterns=[
    path('', views.fun, name='fun'),
    path("register",views.register,name="register"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name='logout'),
    path("details/<int:myid>",views.details,name='details'),
    path("search/details/<int:myid>",views.details,name='details'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
   
    path("cart",views.add_cart,name="cart"),
    path("get_cart_data",views.get_cart_data,name="get_cart_data"),
    path("change_quan",views.change_quan,name="change_quan"),
    path('process_payment',views.process_payment,name="process_payment"),
    path('payment_done',views.payment_done,name="payment_done"),
    path('payment_cancelled',views.payment_cancelled,name="payment_cancelled"),
    path('details/process_payment',views.process_payment,name="process_payment"),
    ]

 