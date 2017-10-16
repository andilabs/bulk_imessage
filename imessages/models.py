# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from clients.models import ClientPhone
from utils.models import TimeStampedModel


class Message(TimeStampedModel):
    send_at = models.DateTimeField(null=True)
    content = models.CharField(max_length=160)
    phone = models.ForeignKey(ClientPhone)

    @property
    def is_sent(self):
        return bool(self.send_at)
