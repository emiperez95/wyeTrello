from django.contrib import admin
from .models import MiniUser, Album


@admin.register(MiniUser)
class userAdmin(admin.ModelAdmin):
    pass


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    pass
