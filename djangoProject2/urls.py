from django.contrib import admin
from django.urls import path

from app01 import views, account

urlpatterns = [
    path('add/', views.add),
    path('', views.giao),
    path('admin/go/', views.admin),
    path("admin/<name>/delete/", views.delete),
    path("login/", account.login)
]
