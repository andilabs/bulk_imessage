# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from utils.models import TimeStampedModel


class Client(TimeStampedModel):
    raw_vcard = models.TextField()
    label = models.CharField(max_length=250)

    def __unicode__(self):
        return self.label


class ClientPhone(TimeStampedModel):
    client = models.ForeignKey(Client)
    phone_number = PhoneNumberField()

    def __unicode__(self):
        return "{}: {}".format(self.client.label, str(self.phone_number))