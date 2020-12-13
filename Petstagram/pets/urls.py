from django.urls import path

from Petstagram.pets.views import details_or_comment_pet, like_pet, delete_pet, \
    PetsListView, CreatePetView, UpdatePetView

urlpatterns = [
    path('', PetsListView.as_view(), name='list pets'),
    path('detail/<int:pk>/', details_or_comment_pet, name='pet details or comment'),
    path('like/<int:pk>/', like_pet, name='like pet'),
    path('edit/<int:pk>/', UpdatePetView.as_view(), name='edit pet'),
    path('delete/<int:pk>/', delete_pet, name='delete pet'),
    path('create/', CreatePetView.as_view(), name='create pet'),
]
