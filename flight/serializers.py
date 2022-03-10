import django


from rest_framework import serializers

from .models import *

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ("id", "first_name","last_name","email","date_of_birth","gender")

class FlightTicketSerializer(serializers.ModelSerializer):
    passenger = PassengerSerializer()
    class Meta:
        model = FlightTicket
        fields = ("id", "passenger","destination","meal","flight_category","coming_from","flight_time","passenger_code")
        extra_kwargs = {
            "passenger_code": {"read_only": True}
        }
    
    def create(self, validated_data):
        passenger_data = validated_data.pop("passenger")
        this_passenger = Passenger.objects.create(
            email=passenger_data["email"],
            first_name=passenger_data["first_name"],
            last_name=passenger_data["last_name"],
            date_of_birth=passenger_data["date_of_birth"],
            gender=passenger_data["gender"]
        )
        this_passenger.save()
        new_flight_ticket = FlightTicket.objects.create(
            passenger=this_passenger,
            destination=validated_data["destination"],
            meal=validated_data["meal"],
            flight_category=validated_data["flight_category"],
            flight_time=validated_data["flight_time"],
            coming_from=validated_data["coming_from"]
        )
        new_flight_ticket.save()
        return new_flight_ticket


    def to_representation(self, obj):
        data = super().to_representation(obj)
        data["passenger"] = obj.passenger.first_name + " " +  obj.passenger.last_name 
        data["destination"] = obj.destination.destination
        data["meal"] =  obj.meal.type
        data["flight_category"] = obj.flight_category.category
        data["coming_from"] = obj.coming_from.destination

        return data
    