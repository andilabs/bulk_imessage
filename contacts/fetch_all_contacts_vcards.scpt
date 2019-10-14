#!/usr/bin/osascript
tell application "Contacts"
	set all_contacts_str to ""
	repeat with theItem in people
		set all_contacts_str to all_contacts_str & (vcard of theItem as text)
	end repeat
   return all_contacts_str
end tell
