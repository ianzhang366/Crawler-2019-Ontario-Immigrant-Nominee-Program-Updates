import json
from log_control import log_main
logger = log_main('log_pnp_json_hander')

def save_dict_to_json(target_dict, json_file):
	logger.info('ENTRY: save_dict_to_json() json_file: '+ json_file)
	_json = json.dumps(target_dict)
	with open(json_file, 'w') as f:
		f.write(_json)
	f.close()

def read_from_traget(json_file):
	logger.info('ENTRY: read_from_traget() json_file: '+ json_file)
	target_dict = json.load(open(json_file))
	return target_dict