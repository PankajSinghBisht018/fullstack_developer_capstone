from django.contrib import admin
from .models import CarMake, CarModel

# Register your models here.

# CarModelInline class



# Registering CarMake and CarModel with Django admin

admin.site.register(CarMake)
admin.site.register(CarModel)


# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
