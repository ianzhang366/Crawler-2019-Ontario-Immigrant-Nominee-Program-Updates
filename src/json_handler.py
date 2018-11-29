"""
save post to disk
eg:
past_post={
    shorten_msg:timeStamp[string] 
    }
"""
import json
from log_control import log_main
LOGGER = log_main('log_pnp_json_hander')

def save_dict_to_json(target_dict, json_file):
    """
    Save python dictionary to a file
    Input: target_dict(dict), json_file(string) json_file, which is the file path
    Return: Boolean, if save success returns True
    """
    LOGGER.info('ENTRY')
    LOGGER.debug('save_dict_to_json() json_file: '+ json_file)
    _json = json.dumps(target_dict)
    try:
        with open(json_file, 'w') as f:
            f.write(_json)
        return True
        LOGGER.info('EXIT')
    except Exception as err:
        LOGGER.exception(err)


def read_from_traget(json_file):
    """
    Read a JSON file and convert it to a python dictionary
    Input: json_file(string) json_file, which is the file path
    Return: target_dict(dict)
    """
    LOGGER.info('ENTRY')
    LOGGER.debug('read_from_traget() json_file: '+ json_file)
    target_dict = json.load(open(json_file))
    LOGGER.debug('read_from_traget() target_dict: '+ target_dict)
    LOGGER.info('EXIT')
    
    return target_dict