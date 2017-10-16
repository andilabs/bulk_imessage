#!/usr/bin/osascript
on run {phoneNumber, message}
	tell application "Messages"
    send message to buddy phoneNumber of service "SMS"
	end tell
end run