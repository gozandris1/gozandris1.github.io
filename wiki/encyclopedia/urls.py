from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:pagename>", views.loadpage, name="wiki"),
    path("search/",views.search, name="search"),
    path("newpage",views.createpage, name="NewPage"),
    path("random", views.randpage, name="randompage"),
    path("wiki/<str:pagename>/edit", views.editpage, name="edit"),
    path("wiki/<str:pagename>/save", views.savepage, name="save")
]
