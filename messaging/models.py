from django.db import models

from clients.models import ClientPhone, Client
from utils.models import TimeStampedModel


class DistributionList(TimeStampedModel):
    label = models.CharField(max_length=160)
    members = models.ManyToManyField(ClientPhone)

    def __str__(self):
        return self.label


class Message(TimeStampedModel):
    send_at = models.DateTimeField(null=True)
    content = models.CharField(max_length=160)
    phone = models.ForeignKey(ClientPhone,
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True)
    distribution_list = models.ForeignKey(DistributionList,
                                          on_delete=models.SET_NULL,
                                          null=True,
                                          blank=True)

    @property
    def is_sent(self):
        return bool(self.send_at)
