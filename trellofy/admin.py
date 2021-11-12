from django.contrib import admin
from .models import miniUser, album

# Register your models here.


@admin.register(miniUser)
class userAdmin(admin.ModelAdmin):
    pass


@admin.register(album)
class albumAdmin(admin.ModelAdmin):
    pass
