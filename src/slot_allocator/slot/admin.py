from django.contrib import admin
from .models import UserSlot



class SlotAdmin(admin.ModelAdmin):
    # readonly_fields = ('id',)
    pass

admin.site.register(UserSlot, SlotAdmin)

