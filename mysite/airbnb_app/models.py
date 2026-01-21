from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18),
                                           MaxValueValidator(90)],
                                           null=True, blank=True)
    user_image = models.ImageField(upload_to='user_photo', null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    password = models.CharField(max_length=40)
    RoleChoices = (
    ('client','client'),
    ('ghost','ghost'),
    ('admin','admin'),
    )
    role_user = models.CharField(max_length=20, choices=RoleChoices, default='client')
    registered_date = models.DateField(auto_now_add=True)
    avatar =models.ImageField(upload_to='avatar_images', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class City(models.Model):
    city_image = models.ImageField(upload_to='city_images')
    city_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.city_name}, {self.city_image}'


class Service(models.Model):
    service_image = models.ImageField(upload_to='service_images')
    service_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.service_name}, {self.service_image}'


class Property(models.Model):
    property_name = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=100)
    property_stars = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    service = models.ManyToManyField(Service)
    address = models.CharField(max_length=255)
    price_per_night = models.CharField(max_length=255)
    property_type = models.CharField(max_length=20)
    rules = models.CharField(max_length=50, blank=True)
    max_guests = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    owner = models.ForeignKey( UserProfile, on_delete=models.CASCADE, related_name='properties')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.property_name


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return f'{self.property}, {self.image}'


class Room(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    room_number = models.PositiveSmallIntegerField()
    price = models.PositiveSmallIntegerField()
    RoomStatusChoices = (
    ('Занят', 'Занят'),
    ('Забронировано', 'Забронировано'),
    ('Свободен', 'Свободен'))
    room_status = models.CharField(max_length=30, choices=RoomStatusChoices)
    description = models.TextField()

    def __str__(self):
        return f'{self.property}, {self.room_number}'


class RoomImage(models.Model):
    room = models.ForeignKey(Room, related_name='rooms', on_delete=models.CASCADE)
    room_image = models.ImageField(upload_to='room_images/')

    def __str__(self):
        return f'{self.room}, {self.room_image}'


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    comment = models.TextField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.property}, {self.user}'

class Booking(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.property}, {self.user}, {self.room}'

class Amenity(models.Model):
    amenity_name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='icon_image')
    property = models.ManyToManyField(Property)


    def __str__(self):
        return self.amenity_name

