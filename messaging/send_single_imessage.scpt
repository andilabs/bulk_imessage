#!/usr/bin/osascript
on run {phoneNumber, message, serviceName}
	tell application "Messages"
		send message to buddy phoneNumber of service serviceName
	end tell
end run
