from django.db import models
from django.utils.timezone import now

class CarMake(models.Model):
    Name = models.CharField(null=False, max_length=30, default='Ferrari')
    Description = models.CharField(null=False, max_length=30, default='Ford Car')
    
    # Create a toString method for object string representation
    def __str__(self):
        return self.Name + " " + self.Description

class CarModel(models.Model):
    CarMake = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    DealerID = models.IntegerField()
    Name = models.CharField(null=False, max_length=30, default='Focus')
    SEDAN = 'sedan'
    SUV = 'suv'
    VAN = 'van'
    MUSCLE = 'muscle'
    SPORT = 'sport'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (VAN, 'Van'),
        (MUSCLE, 'Muscle'),
        (SPORT, 'Sport')
    ]
    Type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default="Focus"
    )
    Year = models.DateField(null=True)
    
    # Create a toString method for object string representation
    def __str__(self):
        return str(self.DealerID) + ", " + self.Name + ", " + self.Type + ", " + str(self.Year)


class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:

    def __init__(self, dealership, purchase, name, id, review, purchase_date, car_make, car_model, car_year, sentiment):
        self.dealership = dealership
        self.purchase = purchase
        self.name = name
        self.id = id
        self.review = review
        self.purhase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment

    def __str__(self):
        return "Reviewer: " + self.name + ", make: " + self.car_make + ", model: " + self.car_model + ", dealership: " + self.dealership + ", review: " + self.review