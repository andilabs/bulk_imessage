tell application "Messages"
	set targetService to 1st service whose service type = iMessage
  return get name of targetService
end tell
-- returns smth like E:yourAppleIdUsedWithImessage@example.com