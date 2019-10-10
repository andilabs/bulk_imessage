import logging
import phonenumbers
from django.conf import settings

from django.core.management.base import BaseCommand
from phonenumbers import NumberParseException

from clients.models import Client, ClientPhone
from clients.fetch_contacts import (
    fetch_all_contacts_vcards,
    get_list_of_vcards_strings,
    get_list_of_vcards_objects
)


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @staticmethod
    def ascii_only(input_string):
        return ''.join([i for i in input_string if ord(i) < 128])

    def update_or_create_client_emails(self, client, vcard_object):
        for email in vcard_object.email_list:
            print(email.value)

    def update_or_create_client_phones(self, client, vcard_object):
        for phone in vcard_object.tel_list:
            cleaned_phone = phone.value
            try:
                cleaned_phone = phonenumbers.parse(cleaned_phone, "PL")
            except NumberParseException as e:
                logger.warning(
                    'Not able to parse this as phone number: %s',
                    cleaned_phone
                )
                continue
            if cleaned_phone.italian_leading_zero and settings.DEFAULT_REGION != 'IT':
                cleaned_phone.italian_leading_zero = False

            cleaned_phone = phonenumbers.format_number(cleaned_phone,
                                                       phonenumbers.PhoneNumberFormat.E164)
            try:
                ClientPhone.objects.update_or_create(
                    client_id=client.id, phone_number=cleaned_phone
                )
            except ValueError as e:
                logger.warning(
                    'Could NOT create ClientPhone instance for %s',
                    cleaned_phone
                )
                pass

    def handle(self, *args, **options):
        list_of_vcards_objects = get_list_of_vcards_objects(
            get_list_of_vcards_strings(fetch_all_contacts_vcards())
        )
        print("vcards count: ", len(list_of_vcards_objects))
        print("unique n.value: ", len(set([str(i.n.value) for i in list_of_vcards_objects])))
        for i, vcard_object in enumerate(list_of_vcards_objects):
            client, created = Client.objects.update_or_create(
                label=str(vcard_object.n.value).strip(), defaults={
                    'raw_vcard': vcard_object
                }
            )

            if hasattr(vcard_object, 'tel_list'):
                self.update_or_create_client_phones(client, vcard_object)
            if hasattr(vcard_object, 'email_list'):
                self.update_or_create_client_emails(client, vcard_object)

