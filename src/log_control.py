import logging
import os,sys

log_base_level = logging.DEBUG #console, console and stream is equal
log_to_file = logging.INFO #log file
print_console = False # whether print log info at console
os.chdir(sys.path[0])
######################### Logging ##########################
def log_main(log_name, log_file= os.path.abspath('..') + '/output/log_daily.log'):
    # print log_file
    logger = logging.getLogger(log_name)
    logger.setLevel(log_base_level) #at root log level

    # format is time, thread id, module name, function name, line number, message
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d:%(levelname)s:%(module)s:%(funcName)s:%(lineno)d:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    #log to admin file
    file_handler = logging.FileHandler(log_file) # Handler is a router for logging
    file_handler.setLevel(log_to_file) # log level of this specific handler
    file_handler.setFormatter(formatter) # set format for this specific handler

    #hook the handlers to log
    logger.addHandler(file_handler)

    if print_console:
        #log to console
        stream_handler = logging.StreamHandler() #route to concole at the mean time the log be put to the other handlers still
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    # logger.info('Log_file_path: ' + log_file)
    return logger

if __name__ == '__main__':
    log_main('a', log_file='/home/ianZhang/pnp_monitor/src/output/log_daily.log')


