from django.urls import path
from .views import RegisterView, CustomLoginView, LogoutView
from .views import (UserProfileAPIView, UserProfileCreateAPIView, UserProfileListAPIView,
                    BuyApartmentListAPIView, RentApartmentListAPIView, ApartmentDetailAPIView, ApartmentCreateAPIView,
                    AgentListAPIView, AgentDetailAPIView,
                    UserPropertiesAPIView,
                    ReviewListCreateAPIView,
                    FavoriteItemSerializerAPIView)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('profile/', UserProfileListAPIView.as_view(), name = 'user_profile'),
    path('profile/<int:pk>/', UserProfileAPIView.as_view(), name = 'profile_detail'),
    path('create_profile/', UserProfileCreateAPIView.as_view(), name = 'create_profile'),

    path('buy_apartments/', BuyApartmentListAPIView.as_view(), name = 'buy_apartments'),
    path('rent_apartments/', RentApartmentListAPIView.as_view(), name = 'rent_apartments'),
    path('apartments/<int:pk>/', ApartmentDetailAPIView.as_view(), name = 'apartment_details'),
    path('create_apartment/', ApartmentCreateAPIView.as_view(), name = 'create_apartment'),

    path('user_properties/', UserPropertiesAPIView.as_view(), name = 'user_properties'),

    path('agents/', AgentListAPIView.as_view(), name = 'agents'),
    path('agents/<int:pk>/', AgentDetailAPIView.as_view(), name = 'agent_detail'),

    path('reviews/', ReviewListCreateAPIView.as_view(), name = 'review_list'),
    path('favorite_items/', FavoriteItemSerializerAPIView.as_view(), name = 'favorite_items'),
]
