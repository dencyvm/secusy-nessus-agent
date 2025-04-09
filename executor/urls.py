from django.urls import path
from . import views



urlpatterns = [
    path('scan', views.scan_list),
    path('scan-detailpage', views.scan_detail_page),
    path('scan-delete',views.delete)
]