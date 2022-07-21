from django.contrib import admin
from .models import CarMake, CarModel

class CarModelInline(admin.StackedInline):
    model = CarModel 
    extra = 1

class MakeAdmin(admin.ModelAdmin):
    fields = ['Name', 'Description']
    inlines = [CarModelInline]

admin.site.register(CarMake, MakeAdmin)
# admin.site.register(CarModel)

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
