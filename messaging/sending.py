import os
import subprocess

from typing import Optional

from clients.models import ClientPhone
from messaging.models import DistributionList

COMMAND_TEMPLATE = u"osascript {applescript_filename} {to_phone_number} {content}"


def send_message(content: str, client_phone: Optional[ClientPhone] = None,
                 distribution_list: Optional[DistributionList] = None):
    phone_numbers = set()
    if client_phone:
        phone_numbers.add(str(client_phone.phone_number))
    if distribution_list:
        phone_numbers.update(
            tuple([
                str(member.phone_number) for member
                in distribution_list.members.all()
            ])
        )
    for phone in phone_numbers:
        send_single_message(content, to_phone_number=phone)


def send_single_message(content, to_phone_number):
    cmd = COMMAND_TEMPLATE.format(
        applescript_filename='send_single_imessage.scpt',
        to_phone_number=to_phone_number,
        content=content
    )
    cwd = '/'.join(os.path.realpath(__file__).split('/')[:-1])
    print(cwd)
    args = cmd.split(' ', 3)
    subprocess.Popen(args, cwd=cwd)

