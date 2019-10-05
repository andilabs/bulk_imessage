# bulk_imessage 👩‍💻👨‍💻✉📲

## send iMessage/SMS in automated bulk way from Mac to your contacts (applescript behind)
## fetch all your Contacts (applescript behind)

⚠ LIMITATION: due to Apple policy you can not write iMessage if the thread in iMessage on your Mac isn't already started with certain contact
create_clients.py


## getting started

* create virtualenv
* activate virtualenv
* pip install -r requirements.txt
* create super user https://docs.djangoproject.com/en/2.2/intro/tutorial02/#creating-an-admin-user
* import contacts - run the `./manage.py fetch_contacts.py` you will be warned by apple script, that terminal wants access to contacts - you have to confirm
* start development server https://docs.djangoproject.com/en/2.2/intro/tutorial02/#start-the-development-server
* go to http://127.0.0.1:8000/admin/imessages/message/ login and start creating and sending messages - the send option is available as bulk action in list view of messages. Only for message with status sent=False the message will be send to avoid sending duplicates. When sending message you will be warned first time by applescript to allow it to terminal.
