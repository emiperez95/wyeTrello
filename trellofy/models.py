from django.db import models
from django.urls import reverse
from django import forms
from django.utils.translation import gettext_lazy as _

import datetime

# Create your models here.


class miniUser(models.Model):

    name = models.CharField(_("user name"), max_length=50)
    trelloKey = models.CharField(_("trello key"), max_length=50)
    date = models.DateTimeField(_("date added"), auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name = _("miniUser")
        verbose_name_plural = _("miniUsers")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("miniUser_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        self.date = datetime.datetime.now()
        super().save(*args, **kwargs)


class album(models.Model):

    name = models.CharField(_("album_name"), max_length=50)
    artist = models.CharField(_("artist name"), max_length=50)
    user = models.ForeignKey("miniUser", verbose_name=_("user"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("album")
        verbose_name_plural = _("albums")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("album_detail", kwargs={"pk": self.pk})


class userForm(forms.ModelForm):
    class Meta:
        model = miniUser
        fields = ('name', 'trelloKey')
