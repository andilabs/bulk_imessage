# -*- coding: utf-8 -*-
import string

from django.core.management.base import BaseCommand

from clients.models import Client, ClientPhone
from clients.fetch_contacts import fetch_all_contacts_vcards, get_list_of_vcards_strings, get_list_of_vcards_objects


class Command(BaseCommand):

    @staticmethod
    def ascii_only(input_string):
        return ''.join([i for i in input_string if ord(i) < 128])

    def handle(self, *args, **options):
        Client.objects.all().delete()
        all_vcards_string = fetch_all_contacts_vcards()
        list_of_vcards_strings = get_list_of_vcards_strings(all_vcards_string)
        list_of_vcards_objects = get_list_of_vcards_objects(list_of_vcards_strings)

        for vcard_str, vcard_object in zip(list_of_vcards_strings, list_of_vcards_objects):
            c = Client.objects.create(label=str(vcard_object.n.value).strip(), raw_vcard=vcard_object)
            if hasattr(vcard_object, 'tel_list'):
                for phone in vcard_object.tel_list:
                    if '*31#' in phone.value:
                        continue
                    cleaned_phone = self.ascii_only(phone.value).replace(' ', '')
                    if '+' not in cleaned_phone:
                        cleaned_phone = '+48{}'.format(cleaned_phone)
                    ClientPhone.objects.create(client=c, phone_number=cleaned_phone)
