from django.contrib import admin

# Register your models here.
from pets.models import Pet, Like


class PetAdmin(admin.ModelAdmin):
    list_display = ('type', 'name')
    list_filter = ('type',)


admin.site.register(Pet, PetAdmin)
admin.site.register(Like)
