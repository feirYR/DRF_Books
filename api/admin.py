from django.contrib import admin

# Register your models here.
from api import models

admin.site.register(models.Authors)
admin.site.register(models.Press)
admin.site.register(models.Books)
admin.site.register(models.AuthorDetail)