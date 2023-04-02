from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers
from . import views

r = routers.DefaultRouter()
r.register('nguoidung', views.NguoiDungViewSet)
r.register('thucdon', views.ThucDonViewSet)
r.register('monan', views.MonAnViewSet)
r.register('sanhcuoi', views.SanhCuoiViewSet)
r.register('dichvu', views.DichVuViewSet)
r.register('binhluan', views.BinhLuanViewSet)

urlpatterns = [
    path('', include(r.urls)),
]