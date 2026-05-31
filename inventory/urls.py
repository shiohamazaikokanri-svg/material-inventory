from django.urls import path

from . import views


app_name = "inventory"

urlpatterns = [
    path("", views.material_list, name="material_list"),
    path("import/", views.import_excel, name="import_excel"),
]
