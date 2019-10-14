import logging
from typing import Sequence

import phonenumbers
from django.conf import settings

from django.core.management.base import BaseCommand
from phonenumbers import NumberParseException
from contrib.applescript import osascript
import vobject

from contacts.models import Contact, ContactPhone
from messaging.sending import get_buddy_preferred_service

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @staticmethod
    def fetch_all_contacts_vcards() -> str:
        # TODO this slow, as is slow but maybe can do it anyway
        #  faster by going one by one spawned in parallel
        all_vcards_string = osascript(
            'contacts/fetch_all_contacts_vcards.scpt')
        return str(all_vcards_string)

    @staticmethod
    def get_list_of_vcards(all_vcards_string) -> Sequence[str]:
        split_by = '\nEND:VCARD'
        return [i + split_by for i in all_vcards_string.split(split_by)][:-1]

    @staticmethod
    def get_list_of_vcards_objects(all_vcards_strings_list) -> Sequence[vobject.vCard]:
        return [vobject.readOne(i) for i in all_vcards_strings_list]

    @staticmethod
    def ascii_only(input_string):
        return ''.join([i for i in input_string if ord(i) < 128])

    @staticmethod
    def update_or_create_contact_emails(contact, vcard_object):
        # TODO implement it create models for ContactPhone
        for email in vcard_object.email_list:
            print(email.value)

    @staticmethod
    def update_or_create_contact_phones(contact, vcard_object):
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
                ContactPhone.objects.update_or_create(
                    contact_id=contact.id, phone_number=cleaned_phone,
                    defaults={
                        'service': get_buddy_preferred_service(cleaned_phone)
                    }
                )
            except ValueError as e:
                logger.warning(
                    'Could NOT create ContactPhone instance for %s',
                    cleaned_phone
                )
                pass

    def handle(self, *args, **options):
        list_of_vcards_objects = self.get_list_of_vcards_objects(
            self.get_list_of_vcards(self.fetch_all_contacts_vcards())
        )
        for i, vcard_object in enumerate(list_of_vcards_objects):
            contact, created = Contact.objects.update_or_create(
                label=str(vcard_object.n.value).strip(), defaults={
                    'raw_vcard': vcard_object
                }
            )

            if hasattr(vcard_object, 'tel_list'):
                self.update_or_create_contact_phones(contact, vcard_object)
            if hasattr(vcard_object, 'email_list'):
                self.update_or_create_contact_emails(contact, vcard_object)

