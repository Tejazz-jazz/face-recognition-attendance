from django.contrib import admin
from django.urls import path
from attendance import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('recognize/', views.recognize, name='recognize'),
]
