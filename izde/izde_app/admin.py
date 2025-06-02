from django.contrib import admin
# from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin
from .models import UserProfile, City, Home, Apartment, ApartmentImages, UserProperties, Company, AgentProfile, User, Review, Favorite, FavoriteItem


admin.site.register(City)
admin.site.register(Home)
admin.site.register(UserProperties)
admin.site.register(Company)
admin.site.register(Review)
admin.site.register(User)
admin.site.register(AgentProfile)
admin.site.register(UserProfile)
admin.site.register(Favorite)
admin.site.register(FavoriteItem)


class ApartmentImagesInlines(admin.TabularInline):
    model = ApartmentImages
    extra = 1

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    inlines = [ApartmentImagesInlines]
