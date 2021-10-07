"""Box urls"""

# Django 
from django.urls import path


# views
from yubi.boxes.views import list_box, create_box

urlpatterns = [
    path('boxes/', list_box),
    path('boxes/create/', create_box),
]

