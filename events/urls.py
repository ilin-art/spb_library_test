from django.urls import path

from .views import CreateUserView, EventView


urlpatterns = [
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('event/', EventView.as_view(), name='event'),
]
