from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from contacts.constants import SERVICE_CHOICES, SMS
from utils.models import TimeStampedModel


class Contact(TimeStampedModel):
    raw_vcard = models.TextField()
    label = models.CharField(max_length=250)

    def __str__(self):
        return self.label


class ContactPhone(TimeStampedModel):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    phone_number = PhoneNumberField()
    service = models.IntegerField(choices=SERVICE_CHOICES, default=SMS)

    def __str__(self):
        return "{}: {}".format(self.contact.label, str(self.phone_number))
