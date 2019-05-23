from django.contrib import admin
from .models import *

admin.site.site_header = 'SYS Administration'

admin.site.register(Student)
admin.site.register(UsDistance)
admin.site.register(CurrentId)
admin.site.register(ArduScore)