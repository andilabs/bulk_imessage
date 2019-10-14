from unittest.mock import patch
from django.core.management import call_command
from django.test import TestCase
from contacts.management.commands import create_contacts

from contacts.models import Contact

VCARDS = """BEGIN:VCARD\r\nVERSION:3.0\r\nPRODID:-//Apple Inc.//Mac OS X 10.15//EN\r\nN:;Falla Warszawa 🌯;;;\r\nFN:Falla Warszawa 🌯\r\nTEL;type=pref:517161727\r\nCATEGORIES:card\r\nUID:504D0ED4-EC58-443F-A757-EB0492A614A4\r\nX-ABUID:954B3EB0-2021-4BC7-968C-DD72892EB08A:ABPerson\r\nEND:VCARD\r\n, BEGIN:VCARD\r\nVERSION:3.0\r\nPRODID:-//Apple Inc.//Mac OS X 10.15//EN\r\nN:;Momencik Buritto 🌮;;;\r\nFN:Momencik Buritto 🌮\r\nTEL;type=pref:536080622\r\nCATEGORIES:card\r\nUID:AC087E48-AFE9-400B-B8D8-3B720189F8FC\r\nX-ABUID:5B9112D1-F95E-43D2-B26D-45C73307A6B8:ABPerson\r\nEND:VCARD\r\n, BEGIN:VCARD\r\nVERSION:3.0\r\nPRODID:-//Apple Inc.//Mac OS X 10.15//EN\r\nN:Kostański;Andrzej;;;\r\nFN:Andrzej Kostański\r\nX-ABUID:82CCB133-5962-4576-A450-A1BCA59ADE79:ABPerson\r\nEND:VCARD"""


class TestCommands(TestCase):

    @patch.object(create_contacts.Command, 'fetch_all_contacts_vcards', return_value=VCARDS)
    def test_mytest(self, _):
        call_command('create_contacts')
        self.assertEqual(Contact.objects.count(), 3)
