from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import (UserProfile, UserProperties, AgentProfile, Apartment, Home, ApartmentImages, Review, FavoriteItem)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
# ----------------------------------------------------------------------
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'password', 'username', 'first_name', 'last_name', 'user_image', 'phone_number', 'email')
        extra_kwargs = {'password': {'write_only': True}}

# owner and agent
class AgentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentProfile
        fields = ('id', 'first_name', 'last_name', 'user_status', 'user_image', 'position')

class AgentDetailSerializer(serializers.ModelSerializer):
    areas_agent = serializers.CharField(source='areas_agent.city')
    company_name = serializers.CharField(source='company.company_name')
    company_logo = serializers.ImageField(source='company.company_logo')
    class Meta:
        model = AgentProfile
        fields = ('id', 'first_name', 'last_name', 'user_status', 'user_image', 'position', 'languages', 'phone_number', 'email', 'areas_agent', 'experience_since', 'company_name', 'company_logo') # active_listing, number_of_properties,

class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = ('home_name',)

class ApartmentImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentImages
        fields = ('apartment_image',)

# apartment
class ApartmentDetailSerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer(read_only=True)
    home_name = HomeSerializer(read_only=True)
    apartment_image = ApartmentImagesSerializer(read_only=True)
    class Meta:
        model = Apartment
        fields = ('id', 'owner', 'home_name', 'apartment_image', 'description_apartment', 'address', 'city', 'for_buy_or_rent', 'count_bathroom', 'count_bedroom', 'minimum_stay', 'deposit', 'price', 'square', 'apartment_type', 'number_of_room', 'bathroom', 'floor', 'floor_of', 'type_of_parking', 'amenities')

class ApartmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = ('id', 'contact_owner', 'home_name', 'apartment_image', 'description', 'address', 'square', 'bathroom', 'bedroom', 'apartment_type', 'for_buy_or_rent', 'floor', 'floor_of', 'city', 'minimum_stay', 'deposit', 'price', 'balkony', 'microwave', 'wifi', 'covered_parking', 'central_heating', 'tv', 'washing_machine', 'air_conditioner', 'smoking_in_the_apartment', 'listen_to_music_loudly')

class UserPropertiesSerializer(serializers.ModelSerializer):
    apartment_name = serializers.CharField(source='apartment.home.home_name', read_only=True)
    price = serializers.IntegerField(source='apartment.price', read_only=True)
    city = serializers.CharField(source='apartment.city.city', read_only=True)
    square = serializers.IntegerField(source='apartment.square', read_only=True)
    bathroom = serializers.CharField(source='apartment.bathroom', read_only=True)
    count_bedroom = serializers.IntegerField(source='apartment.count_bedroom', read_only=True)
    experience_since = serializers.DateField(source='user.agentprofile.experience_since', read_only=True, allow_null=True)
    apartment_image = ApartmentImagesSerializer(read_only=True, many=True)
    user_image = serializers.ImageField(source='user.user_image', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProperties
        fields = ('user_image', 'experience_since', 'first_name', 'last_name', 'phone_number', 'email', 'apartment_name', 'apartment_image', 'price', 'city', 'square', 'bathroom', 'count_bedroom')

# screen Buy
class BuyApartmentSerializer(serializers.ModelSerializer):
    home_name = HomeSerializer(read_only=True)
    apartment_image = serializers.ImageField(read_only=True)
    city = serializers.CharField(source='city.city')
    class Meta:
        model = Apartment
        fields = ('id', 'apartment_type', 'home_name', 'apartment_image', 'price', 'city', 'square', 'count_bathroom', 'count_bedroom')

# screen Rent
class RentApartmentSerializer(serializers.ModelSerializer):
    home_name = HomeSerializer(read_only=True)
    apartment_image = serializers.ImageField(read_only=True)
    city = serializers.CharField(source='city.city')
    class Meta:
        model = Apartment
        fields = ('id', 'apartment_type', 'home_name', 'apartment_image', 'price', 'city', 'square', 'count_bathroom', 'count_bedroom')

# screen Review
class ReviewSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Review
        fields = ('id', 'user', 'apartment', 'text_review', 'stars')

# screen FavoriteItem
class FavoriteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteItem
        fields = ('apartment',)
