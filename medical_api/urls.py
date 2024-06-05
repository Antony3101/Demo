from django.urls import path
from .views import signup, user_login, create_medicine, retrieve_medicine, update_medicine, delete_medicine

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('medicines/', create_medicine, name='create_medicine'),
    path('medicines/<int:pk>/', retrieve_medicine, name='retrieve_medicine'),
    path('medicines/<int:pk>/update/', update_medicine, name='update_medicine'),
    path('medicines/<int:pk>/delete/', delete_medicine, name='delete_medicine'),
]