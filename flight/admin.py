from django.contrib import admin

from .models import *

class PassengerAdmin(admin.ModelAdmin):
    list_display = ("first_name","last_name","email","date_of_birth","gender")


class DestinationAdmin(admin.ModelAdmin):
    list_display = ("destination","code")


class GenderAdmin(admin.ModelAdmin):
    list_display = ("name","code")


class MealAdmin(admin.ModelAdmin):
    list_display = ("type","code")


class FlightCategoryAdmin(admin.ModelAdmin):
    list_display = ("category","code")


class ComingFromAdmin(admin.ModelAdmin):
    list_display = ("destination","code")


admin.site.register(Passenger,PassengerAdmin)
admin.site.register(Destination,DestinationAdmin)
admin.site.register(Gender,GenderAdmin)
admin.site.register(Meal,MealAdmin)
admin.site.register(FlightCategory,FlightCategoryAdmin)
admin.site.register(ComingFrom,ComingFromAdmin)