import logging
import sh


logger = logging.getLogger(__name__)

try:
    osascript = sh.Command("osascript")
except sh.CommandNotFound as e:
    logger.warning('Applescript not available on this platform')
