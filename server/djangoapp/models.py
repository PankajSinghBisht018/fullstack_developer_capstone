# Uncomment the following imports before adding the Model code
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

# Car Make model
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name  # String representation of a CarMake object


# Car Model model
class CarModel(models.Model):
    # Many-To-One relationship with CarMake
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    # Choices for car type
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        # Add more types if needed
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')

    # Year field with range validation
    year = models.IntegerField(
        validators=[
            MaxValueValidator(2023),  # Maximum year value
            MinValueValidator(2015)  # Minimum year value
        ]
    )

    dealer_id = models.IntegerField()  # Refers to a dealer (external DB)

    def __str__(self):
        # String representation combining car make and model
        return f"{self.car_make.name} - {self.name}"
