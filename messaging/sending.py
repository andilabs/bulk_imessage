import collections
from typing import Optional, Sequence, DefaultDict

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
                            service_type=service)


def get_buddy_services(phone_number: str) -> Sequence[str]:
    services = osascript('messaging/get_buddy_services.scpt', phone_number)
    services_list = services.replace('\n', '').split(', ')
    return services_list


def get_all_buddy_services() -> DefaultDict[str, Sequence[str]]:
    sequence_of_handle_followed_by_name_of_service = osascript(
        'messaging/get_all_budies_service_handle.scpt').split(', ')
    handle_end_index = int(
        len(sequence_of_handle_followed_by_name_of_service) / 2)
    services_lookup = collections.defaultdict(list)
    for i in range(handle_end_index):
        services_lookup[
            sequence_of_handle_followed_by_name_of_service[i]
        ].append(sequence_of_handle_followed_by_name_of_service[
            i+handle_end_index].strip())
    return services_lookup


def determine_preferred_service(list_of_services: Sequence[str]) -> int:
    if settings.PREFERRED_SERVICE == constants.iMessage:

        if imessage_service_name in list_of_services:
            return settings.PREFERRED_SERVICE

    return settings.FALLBACK_SERVICE


def get_buddy_preferred_service(phone_number: str) -> int:
    buddy_services = get_buddy_services(phone_number)
    return determine_preferred_service(buddy_services)


def get_service_name_for_imessage() -> str:
    imessage_service_name = osascript(
        'messaging/get_imessage_service_name.scpt')
    return imessage_service_name.strip()


imessage_service_name = get_service_name_for_imessage()


def send_single_message(content: str, to_phone_number: str,
                        service_type: int = settings.FALLBACK_SERVICE):
    if service_type == constants.iMessage:
        service_name = get_service_name_for_imessage()
    else:
        service_name = dict(constants.SERVICE_CHOICES)[constants.SMS]
    osascript('messaging/send_single_imessage.scpt',
              to_phone_number,
              content,
              service_name)
