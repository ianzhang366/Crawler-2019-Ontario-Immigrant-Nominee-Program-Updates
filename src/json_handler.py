import json
from log_control import log_main
logger = log_main('log_pnp_json_hander')

def save_dict_to_json(target_dict, json_file):
	"""
	Save python dictionary to a file
	Input: target_dict(dict), json_file(string) json_file, which is the file path
	Return: Boolean, if save success returns True
	"""
	logger.info('ENTRY')
	logger.debug('save_dict_to_json() json_file: '+ json_file)
	_json = json.dumps(target_dict)
	try:
		with open(json_file, 'w') as f:
			f.write(_json)
		return True
		logger.info('EXIT')
	except Exception as err:
		logger.exception(err)


def read_from_traget(json_file):
	"""
	Read a JSON file and convert it to a python dictionary
	Input: json_file(string) json_file, which is the file path
	Return: target_dict(dict)
	"""
	logger.info('ENTRY')
	logger.debug('read_from_traget() json_file: '+ json_file)
	target_dict = json.load(open(json_file))
	logger.debug('read_from_traget() target_dict: '+ target_dict)
	logger.info('EXIT')
	return target_dict