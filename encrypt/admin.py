from django.contrib import admin
from .models import Hashes, Uploads
from .models import Uploads
from .functions import *
# Register your models here.


class AdminUploads(admin.ModelAdmin):
    list_display = ('text_file', 'date_created')


admin.site.register(Uploads, AdminUploads)
