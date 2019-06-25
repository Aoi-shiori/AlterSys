from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Alter_managment

# Register your models here.

class Alter_managment_resources(resources.ModelResource):
    class Meta:
        model = Alter_managment


@admin.register(Alter_managment)
class Alter_managment_Admin(ImportExportModelAdmin):
    resource_class = Alter_managment_resources

