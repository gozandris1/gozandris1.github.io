from django.contrib import admin
from .models import Category, Listing, User
# Register your models here.

class ListingInline(admin.TabularInline):
    model = Listing

class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = [
        ListingInline
    ]

admin.site.register(Category)
admin.site.register(Listing)
#admin.site.register(User, UserAdmin)
admin.site.register(User)