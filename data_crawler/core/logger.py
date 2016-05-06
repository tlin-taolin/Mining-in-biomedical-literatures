import logging
import logging.config

class Logger:
  @staticmethod
  def get_logger(name=None, level=logging.DEBUG):
    logging.config.fileConfig('settings/logging.conf')
    return logging.getLogger(name)
