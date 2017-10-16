# -*- coding: utf-8 -*-
import os
import subprocess
import vobject

COMMAND_TEMPLATE = u"osascript {applescript_filename}"


def fetch_all_contacts_vcards():
    cmd = COMMAND_TEMPLATE.format(
        applescript_filename='fetch_all_contacts_vcards.scpt',
    )
    cwd = '/'.join(os.path.realpath(__file__).split('/')[:-1])
    all_vcards_string = subprocess.check_output([cmd], cwd=cwd, shell=True)
    return all_vcards_string


def get_list_of_vcards_strings(all_vcards_string):
    split_by = '\r\nEND:VCARD'
    return [i+split_by for i in all_vcards_string.split(split_by)][:-1]


def get_list_of_vcards_objects(all_vcards_strings_list):
    return [vobject.readOne(i) for i in all_vcards_strings_list]
