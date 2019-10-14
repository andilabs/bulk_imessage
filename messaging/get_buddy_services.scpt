on run {phoneNumber}
	tell application "Messages" to return name of service of (buddies whose handle contains phoneNumber)
end run
