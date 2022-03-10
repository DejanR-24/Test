from django.db import models
from datetime import date, time

from .utils import Util

class Gender(models.Model):
    name = models.CharField(max_length=10)
    code = models.CharField(max_length=1)

class Passenger(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    date_of_birth = models.DateField()
    gender = models.ForeignKey(Gender, to_field="id",on_delete=models.CASCADE)


class Destination(models.Model):
    destination = models.CharField(max_length=20)
    code = models.CharField(max_length=1)


class Meal(models.Model):
    type = models.CharField(max_length=20)
    code = models.CharField(max_length=1)

class FlightCategory(models.Model):
    category = models.CharField(max_length=20)
    code = models.CharField(max_length=1)

class ComingFrom(models.Model):
    destination = models.CharField(max_length=20)
    code = models.CharField(max_length=3)

class FlightTicketManager(models.Manager):
    def create(self, **obj_data):
        passenger = obj_data["passenger"]
        destination = obj_data["destination"]
        gender = passenger.gender
        meal =obj_data["meal"]
        flight_category=obj_data["flight_category"]
        coming_from = obj_data["coming_from"]
        
        passenger_code = ""
        
        def calculate_age(born):
            today = date.today()
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

        flight_time = obj_data["flight_time"]
        age=calculate_age(passenger.date_of_birth)
        if(flight_time>time(6,0,0) and flight_time<time(22,0,0)):
            passenger_code = passenger_code + destination.code.upper()
        else:
            passenger_code = passenger_code + destination.code
        gender_code = gender.code
        meal_code = meal.code
        if(age>12):
            gender_code = gender_code.upper()
            meal_code = meal_code.upper()
        passenger_code = passenger_code + gender_code + meal_code + flight_category.code + coming_from.code
        obj_data["passenger_code"] = passenger_code

        email_subject = (
                    "Confirmed flight deatils"
                )
        email_body = (
                    "Dear "
                    + passenger.first_name
                    + ",\n\nWe are happy to inform you that you successfully booked your ticket.\nYour passenger_code is : " 
                    + passenger_code
                    + "\n\n Have a good flight! Thanks for using our services"
                )
        send_to = passenger.email
        data = {
                    "email_body": email_body,
                    "send_to": send_to,
                    "email_subject": email_subject,
                }
        Util.send_email(data)

        return super().create(**obj_data)


class FlightTicket(models.Model):
    passenger = models.ForeignKey(Passenger, to_field="id", on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination,to_field="id",on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal,to_field="id",on_delete=models.CASCADE)
    flight_category = models.ForeignKey(FlightCategory,to_field="id", on_delete=models.CASCADE)
    coming_from = models.ForeignKey(ComingFrom,to_field="id",on_delete=models.CASCADE)
    flight_time = models.TimeField()
    passenger_code=models.CharField(max_length=30)

    objects = FlightTicketManager()