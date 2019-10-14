from typing import Optional

from django.conf import settings

from contacts import constants
from contacts.models import ContactPhone
from contrib.applescript import osascript
from messaging.models import DistributionList


def send_message(content: str, contact_phone: Optional[ContactPhone] = None,
                 distribution_list: Optional[DistributionList] = None):
    phone_numbers = dict()
    if contact_phone:
        phone_numbers[str(contact_phone.phone_number)] = contact_phone.service
    if distribution_list:
        phone_numbers.update({
            str(member.phone_number): contact_phone.service
            for member in distribution_list.members.all()})
    for phone, service in phone_numbers.items():
        send_single_message(content,
                            to_phone_number=phone,
                            service_name=service)


def get_buddy_services(phone_number):
    services = osascript('messaging/get_buddy_services.scpt', phone_number)
    services_list = services.replace('\n', '').split(', ')
    return services_list


def get_buddy_preferred_service(phone_number):
    buddy_services = get_buddy_services(phone_number)

    if settings.PREFERRED_SERVICE_NAME == constants.iMessage:
        imessage_service_name = get_service_name_for_imessage()
        if imessage_service_name in buddy_services:
            return settings.PREFERRED_SERVICE_NAME

    return settings.FALLBACK_SERVICE_NAME


def get_service_name_for_imessage():
    imessage_service_name = osascript('messaging/get_imessage_service_name.scpt')
    return imessage_service_name.strip()


def send_single_message(content: str, to_phone_number: str,
                        service_name: str = settings.FALLBACK_SERVICE_NAME):
    if service_name == constants.iMessage:
        service_name = get_service_name_for_imessage()
    osascript('messaging/send_single_imessage.scpt',
              to_phone_number,
              content,
              service_name)
