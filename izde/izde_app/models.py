from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField
from django.core.validators import MinValueValidator, MaxValueValidator


CHOICES_PROPERTY = (('client', 'client'), ('agent', 'agent'))

class UserProfile(AbstractUser):
    user_image = models.ImageField(upload_to='user_images/', blank=True, null=True)
    phone_number = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True)
    created_account = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}'

class City(models.Model):
    city = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'City name: {self.city}'

class Home(models.Model):
    home_name = models.CharField(max_length=20, null=True)

    # функция жазыш керек
    # count_apartments =

    def __str__(self):
        return f'Home name: {self.home_name}'

class Apartment(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE) #
    description_apartment = models.TextField(max_length=500)
    address = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    CHOICES_RENT_OR_BUY = (('buy', 'buy'), ('rent', 'rent'))
    for_buy_or_rent = models.CharField(choices=CHOICES_RENT_OR_BUY, default='rent')
    count_bathroom = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)])
    count_bedroom = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)])
    CHOICES_BATHROOM = (('combined', 'combined'), ('separate', 'separate'))
    bathroom = models.CharField(choices=CHOICES_BATHROOM)
    minimum_stay = models.DateField()
    deposit = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(9999999)])
    price = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(9999999)], blank=True, null=True)
    square = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(999)])
    APARTMENT_TYPE = (('apartment', 'apartment'), ('townhouse', 'townhouse'), ('penthouse', 'penthouse'), ('office', 'office'))
    apartment_type = models.CharField(choices=APARTMENT_TYPE)
    number_of_room = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(999)])
    floor = models.IntegerField(validators=[MaxValueValidator(999)])
    floor_of = models.IntegerField(validators=[MaxValueValidator(999)])
    CHOICES_TYPE_PARKING = (('ground', 'ground'), ('underground', 'underground'), ('no', 'no'))
    type_of_parking = models.CharField(choices=CHOICES_TYPE_PARKING)
    CHOICES_AMENITIES = (
        ('smoking_in_the_apartment', 'smoking_in_the_apartment'),
        ('listen_to_music_loudly', 'listen_to_music_loudly'),
        ('balkony', 'balkony'),
        ('microwave', 'microwave'),
        ('wifi', 'wifi'),
        ('central_heating', 'central_heating'),
        ('tv', 'tv'),
        ('washing_machine', 'washing_machine'),
        ('air_conditioner', 'air_conditioner'),
        ('tableware', 'tableware'),
        ('swimming_pool', 'swimming_pool'),
        ('gym', 'gym'),
        ('workspace', 'workspace'),
        ('pet_friendly', 'pet_friendly'))
    amenities = MultiSelectField(max_length=200, choices=CHOICES_AMENITIES)
    created_by = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'number of room: {self.number_of_room}'

class ApartmentImages(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='apartment_image')
    apartment_image = models.ImageField(blank=True, null=True, upload_to='apartment_images/')

class UserProperties(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)

    def __str__(self):
        return f'Properties: {self.user}'

class Company(models.Model):
    company_name = models.CharField(max_length=20, unique=True)
    company_logo = models.ImageField(upload_to='company_logo/', blank=True, null=True)

    def __str__(self):
        return f'{self.company_name}'

class AgentProfile(UserProfile):
    user_status = models.CharField(choices=CHOICES_PROPERTY, max_length=10, default='agent', editable=False)
    LANGUAGES_AGENT = (('English', 'English'), ('Russian', 'Russian'), ('Kyrgyz', 'Kyrgyz'))
    languages = MultiSelectField(choices=LANGUAGES_AGENT, max_choices=3)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    areas_agent = models.ForeignKey(City, on_delete=models.CASCADE)
    experience_since = models.DateField()
    CHOICES_POSITION = (('expert', 'expert'), ('junior', 'junior'))
    position = models.CharField(choices=CHOICES_POSITION, max_length=20, default='expert')

    class Meta:
        verbose_name = 'Агент'
        verbose_name_plural = 'Агенты'

    def __str__(self):
        return f'Agent name: {self.first_name}'

    # функция жазыш керек
    # active_listing = кайсы домдор менен иштешип атат???
    # number_of_properties = канча дом менен иштешип атат

class User(UserProfile):
    user_status = models.CharField(choices=CHOICES_PROPERTY, max_length=10, default='client', editable=False)

    class Meta:
        verbose_name = 'Клиент/Владелец'
        verbose_name_plural = 'Клиенты/Владельцы'

    def __str__(self):
        return f'Client name: {self.first_name}'

class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    text_review = models.TextField()
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self):
        return f'owner review: {self.user} - star: {self.stars}'

class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'

class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.apartment}'
