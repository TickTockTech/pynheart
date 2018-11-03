import os
import logging
import logging.config

log_config = os.path.abspath(os.path.join(os.path.dirname(__file__), "log.cfg"))
logging.config.fileConfig(log_config)

# create logger
Log = logging.getLogger('gameLog')
