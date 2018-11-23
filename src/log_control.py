import logging
import _config

import sys
sys.path.append(_config.SEN_CONFIG.data_location)
import config

# log_base_level = logging.DEBUG #console, console and stream is equal
# log_to_file = logging.INFO #log file
# print_console = False # whether print log info at console
# print log_base_level
######################### Logging ##########################
def log_main(log_name, log_config= config.LOG_CONFIG):
    # print log_file
    logger = logging.getLogger(log_name)
    logger.setLevel(config.LOG_CONFIG.log_base_level) #at root log level

    # format is time, thread id, module name, function name, line number, message
    formatter = logging.Formatter(config.LOG_CONFIG.content_formate, datefmt=config.LOG_CONFIG.datefmt)

    #log to admin file
    file_handler = logging.FileHandler(config.LOG_CONFIG.location) # Handler is a router for logging
    file_handler.setLevel(config.LOG_CONFIG.log_to_file) # log level of this specific handler
    file_handler.setFormatter(formatter) # set format for this specific handler

    #hook the handlers to log
    logger.addHandler(file_handler)

    if config.LOG_CONFIG.print_console:
        #log to console
        stream_handler = logging.StreamHandler() #route to concole at the mean time the log be put to the other handlers still
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    # logger.info('Log_file_path: ' + log_file)
    return logger

if __name__ == '__main__':
    log_main('a', config.LOG_CONFIG)
    # print config.LOG_CONFIG.location



