#!/usr/bin/osascript
on run {phoneNumber, message}
	tell application "Messages"
	set targetService to 1st service whose service type = iMessage
    send message to buddy phoneNumber of targetService
	end tell
end run