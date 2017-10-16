#!/usr/bin/osascript
tell application "Contacts"
	set myList to name of (people)
	set all_contacts_str to ""
	repeat with theItem in people
		set all_contacts_str to all_contacts_str & (get vcard of theItem)
	end repeat
    return all_contacts_str
end tell