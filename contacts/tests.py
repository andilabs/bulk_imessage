from unittest.mock import patch
from django.core.management import call_command
from django.test import TestCase
from contacts.management.commands import create_contacts

from contacts.models import Contact

VCARDS = """
BEGIN:VCARD
VERSION:3.0
PRODID:-//Apple Inc.//Mac OS X 10.15//EN
N:;Momencik Buritto 🌮;;;
FN:Momencik Buritto 🌮
TEL;type=pref:536080622
CATEGORIES:card
UID:AC087E48-AFE9-400B-B8D8-3B720189F8FC
X-ABUID:5B9112D1-F95E-43D2-B26D-45C73307A6B8:ABPerson
END:VCARD
BEGIN:VCARD
VERSION:3.0
PRODID:-//Apple Inc.//Mac OS X 10.15//EN
N:Kostański;Andrzej;;;
FN:Andrzej Kostański
X-ABUID:82CCB133-5962-4576-A450-A1BCA59ADE79:ABPerson
END:VCARD
"""


class TestCommands(TestCase):

    @patch.object(create_contacts.Command, 'fetch_all_contacts_vcards', return_value=VCARDS)
    def test_mytest(self, _):
        call_command('create_contacts')
        self.assertEqual(Contact.objects.count(), 2)
