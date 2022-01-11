from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('validate_login', views.validate_login),
    path('logout', views.logout),
    path('quotes', views.quotes),
    path('add_quote',views.add_quote),
    path('edit_page/<int:quote_id>',views.edit_page),
    path('edit/<int:quote_id>',views.edit),
    path('delete_quote/<int:quote_id>',views.delete_quote),
    path('user_page/<int:user_id>', views.user_page),
]