from django.contrib import admin
from core import models

# change admin site view
admin.site.site_title = "test"
admin.site.site_header = "test"
admin.site.index_title = "test"

# Register your models here.
admin.site.register(models.Content)
