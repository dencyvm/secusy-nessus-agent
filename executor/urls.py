from django.urls import path
from . import views



urlpatterns = [
    path('scan', views.scan_list),
    path('scan-detailpage', views.scan_detail_page),
    path('scan-delete',views.delete),
    path('scan/<int:scan_id>/pause/', views.pause_scan, name='pause_scan'),
    path('scan/<int:scan_id>/resume/', views.resume_scan, name='resume_scan'),
    path('scan/<int:scan_id>/stop/', views.stop_scan, name='stop_scan'),
]