from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new_wiki/", views.create_entry, name="create_entry"),
    path("edit_entry/<str:title>/", views.edit_entry, name="edit_entry"),
    path("random_entry/", views.random_entry, name="random_entry"),
    path("wiki/<str:title>/", views.entry, name="entry"),
]
