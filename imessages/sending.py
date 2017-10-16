# -*- coding: utf-8 -*-
import os
import subprocess

COMMAND_TEMPLATE = u"osascript {applescript_filename} {to_phone_number} '{content}'"


def send_imessage(to_phone_number, content):
    cmd = COMMAND_TEMPLATE.format(
        applescript_filename='send_single_imessage.scpt',
        to_phone_number=to_phone_number,
        content=content
    )
    cwd = '/'.join(os.path.realpath(__file__).split('/')[:-1])
    subprocess.call(cmd, shell=True, cwd=cwd)