from rest_framework import viewsets, generics, status, permissions
from .models import (UserProfile, UserProperties, AgentProfile, Apartment, Review, FavoriteItem)
from .serializers import AgentListSerializer, AgentDetailSerializer, UserPropertiesSerializer, UserProfileSerializer, ApartmentDetailSerializer, BuyApartmentSerializer, RentApartmentSerializer, ReviewSerializer, FavoriteItemSerializer, UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from .filters import ApartmentFilter


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
# --------------------------------------------------------------------------
class LoginAPIView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = LoginSerializer

class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class UserProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class UserProfileCreateAPIView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class BuyApartmentListAPIView(generics.ListAPIView):
    queryset = Apartment.objects.all()
    serializer_class = BuyApartmentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ApartmentFilter
    ordering_fields = ['created_by']
    ordering = ['created_by']

class RentApartmentListAPIView(generics.ListAPIView):
    queryset = Apartment.objects.all()
    serializer_class = RentApartmentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ApartmentFilter
    ordering_fields = ['created_by']
    ordering = ['created_by']

class ApartmentDetailAPIView(generics.RetrieveAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentDetailSerializer

class ApartmentCreateAPIView(generics.CreateAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentDetailSerializer

    permission_classes = [permissions.IsAuthenticated]

class UserPropertiesAPIView(generics.ListAPIView):
    queryset = UserProperties.objects.all()
    serializer_class = UserPropertiesSerializer

class AgentListAPIView(generics.ListAPIView):
    queryset = AgentProfile.objects.all()
    serializer_class = AgentListSerializer

class AgentDetailAPIView(generics.RetrieveAPIView):
    queryset = AgentProfile.objects.all()
    serializer_class = AgentDetailSerializer

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    permission_classes = [permissions.IsAuthenticated]

class FavoriteItemSerializerAPIView(generics.ListAPIView):
    queryset = FavoriteItem.objects.all()
    serializer_class = FavoriteItemSerializer

    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)
