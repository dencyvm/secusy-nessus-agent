from django.contrib import admin
from django.urls import path,include
from nessusEngine.health_check import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('nessus/', include('executor.urls')),
    path('health-check/', health_check)
]
