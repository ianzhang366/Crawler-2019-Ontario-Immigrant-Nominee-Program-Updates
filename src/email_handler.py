#!/Users/ian.w.zhang@ibm.com/Documents/pnp/pnp_py/lib/python2.7
import datetime as dt
import os,sys, time
from time import gmtime, strftime
from data_logic import parse_pnp_posts, get_time_mark
import platform
from json_handler import save_dict_to_json, read_from_traget
from _email_send_handler import _send_email
from log_control import log_main
logger = log_main('log_pnp_email_handler')
import _config

import sys
sys.path.append(_config.SEN_CONFIG.data_location)
import config

#########################Handle Email Format##########################

def format_post(info, email_source):
	logger.info('ENTRY: format_post()')
	start = '<html><head></head><body>'
	end =   '</body></html>'
	formated =''
	send_from='<p style="color:#FFAA00"><b>' + email_source+ '</b></p>'
	for item in info:
		formated += '<br>'
		formated += '<b>' + item['timeStamp'] + '</b>'
		formated += '<br>'
		for i in item['content']:
			formated += '<p>' + i + '</p>'
			formated += '<br>'
		formated += '<br><br>'
	whole = start+formated+send_from+end
	logger.info('EXIT: format_post() %s', whole[-9:])
	return whole.encode('utf-8')

######################### Email content prep ##########################

######################### Handle Email ##########################

def is_new_email(info, json_file, email_source):
	logger.info('ENTRY: is_new_email()')
	need_to_send = []
	past_posts = read_from_traget(json_file)
	if info:
		for item in info:
			# print item['timeStamp']
			# print item['content']
			msg = '%'.join([i for i in item['content']]).replace(' ','').lower()
			shorten_msg = [msg[i] for i in range(len(msg)) if i % 3 == 0]
			shorten_msg = ''.join(shorten_msg)
			if (shorten_msg in past_posts.keys()) == False:
				past_posts[shorten_msg] = item['timeStamp']
				need_to_send.append(item)
	if need_to_send:
		out_html = format_post(need_to_send, email_source)
		_send_email(out_html)
		logger.info('EXIT: is_new_email() ', out_html[-30:])
	else:
		time_check = dt.datetime.utcnow() - dt.timedelta(0, 4*3600) #utc to ESTs
		flag = 0
		if time_check.hour == 17:
			d_short_msg = str(time_check.year)+str(time_check.month) + str(time_check.day) + str(time_check.hour)
			start = '<html><head></head><body>'
			end =   '</body></html>'
			formated ="<b>We don't have any updates today till the office hour done. But I will keep working during the night!</b>"
			d_msg = start + formated + '<p style="color:#FFAA00"><b>' + email_source+ '</b></p>' + end 
			if (d_short_msg in past_posts.keys()) == False:
				past_posts[d_short_msg] = d_short_msg
				_send_email(d_msg, title= "PNP robot: I'm done for the day!")
				flag = 1
		if time_check.hour == 8:
			d_short_msg = str(time_check.year)+str(time_check.month) + str(time_check.day) + str(time_check.hour)
			start = '<html><head></head><body>'
			end =   '</body></html>'
			formated ="<b>A brand new day, let's see what will happen!</b>"
			d_msg = start + formated + '<p style="color:#FFAA00"><b>' + email_source+ '</b></p>' + end
			if (d_short_msg in past_posts.keys()) == False:
				past_posts[d_short_msg] = d_short_msg
				_send_email(d_msg, title= "PNP robot: Master, I'm about to start the day, hopefully you will have a great day!")
				flag = 1
		logger.info('EXIT: is_new_email() check hour:%s, if sent an email %s',time_check, flag)
	logger.info('EXIT: is_new_email() dont need to send email')
	save_dict_to_json(past_posts, json_file)


def _main():
	time_check = dt.datetime.utcnow() - dt.timedelta(0, 4*3600)
	print 'EST: ', time_check.strftime(config.LOG_CONFIG.datefmt) 
	logger.info('Main: email_handler_main() Run time is EST:%s', time_check.strftime(config.LOG_CONFIG.datefmt))
	json_file = config.OUTPUT.past_posts
	time_mark = get_time_mark()
	info = parse_pnp_posts(time_mark)
# 	print info
	if info:
		if len(info):
			logger.info('ENTRY: email_handler_main() Posts: '+ ' '.join(info[0]['content']))
		else:
			logger.info('ENTRY: email_handler_main() Posts: []')
	else:
		logger.info('ENTRY: email_handler_main() Posts: is NONE')
		logger.info('ENTRY: email_handler_main() JSON Path: '+json_file)
	email_source = platform.uname()[1]
	is_new_email(info, json_file, email_source)
	if info:
		logger.info('EXIT: email_handler_main() Posts: %s', info[-20:])
	else:
		logger.info('EXIT: email_handler_main() Posts: %s', info)

if __name__ == '__main__':
	time_check = dt.datetime.utcnow() - dt.timedelta(0, 4*3600)
	print 'EST: ', time_check.strftime(config.LOG_CONFIG.datefmt) 
	_main()



