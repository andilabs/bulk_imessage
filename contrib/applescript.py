import logging
import sh


logger = logging.getLogger(__name__)

try:
    osascript = sh.Command("osascript")
except sh.CommandNotFound:
    sad_message = 'Sorry you are probably not running OS X and ' \
                  'Applescript is not available on this platform'
    logger.warning(sad_message)
    osascript = sh.Command("echo")
