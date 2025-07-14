from django.contrib import admin
from django.urls import path
from analyzer.views import analyze

urlpatterns = [
    path('admin/', admin.site.urls),
    path('analyze/', analyze),  
]
