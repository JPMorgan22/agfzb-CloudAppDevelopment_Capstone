from django.db import models
from django.utils.timezone import now

class CarMake(models.Model):
    Name = models.CharField(null=False, max_length=30, default='Ford')
    Description = models.CharField(null=False, max_length=30, default='Ford Car')
    
    # Create a toString method for object string representation
    def __str__(self):
        return self.name + " " + self.description

class CarModel(models.Model):
    carMake = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
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


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
