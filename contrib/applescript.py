import logging
import sh


logger = logging.getLogger(__name__)

try:
    osascript = sh.Command("osascript")
except sh.CommandNotFound:
    logger.error('Sorry you are probbably not running OS X and '
                 'Applescript not available on this platform')
