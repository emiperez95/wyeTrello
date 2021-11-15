from django.db import models
from django.urls import reverse
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.


class MiniUser(models.Model):

    name = models.CharField(_("artist name"), max_length=50)
    board_name = models.CharField(_("Board name"), max_length=50)
    trelloToken = models.CharField(_("trello token"), max_length=100)
    spotifyToken = models.CharField(_("spotify token"), max_length=512, default=0)
    date = models.DateTimeField(_("date added"), auto_now=False, auto_now_add=False)
    file = models.FileField(_("Albums file"), null=False, blank=False)

    class Meta:
        verbose_name = _("MiniUser")
        verbose_name_plural = _("MiniUsers")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("MiniUser_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        self.date = timezone.now()
        super().save(*args, **kwargs)


class Album(models.Model):

    name = models.CharField(_("Album name"), max_length=50)
    year = models.CharField(_("Album year"), max_length=5)
    user = models.ForeignKey("MiniUser", verbose_name=_("user"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Album")
        verbose_name_plural = _("Albums")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Album_detail", kwargs={"pk": self.pk})


class UserForm(forms.ModelForm):
    class Meta:
        model = MiniUser
        fields = ('name', 'board_name', 'trelloToken', 'spotifyToken', 'file')
