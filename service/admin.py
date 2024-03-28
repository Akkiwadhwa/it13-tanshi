from django.contrib import admin

# Register your models here.
from .models import item
admin.site.register(item)
from .models import lost_item
admin.site.register(lost_item)
from .models import found_item
admin.site.register(found_item)
from .models import contactenquiry
admin.site.register(contactenquiry)