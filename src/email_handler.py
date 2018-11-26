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




def format_post(pnp_posts, content, email_source):
	"""
	Put up a HTML string 
	Input: pnp_posts(list of dict), content(string, predefined email content), email_source(string) where the email is from
	Return: whole(string, HTML)
	"""
	logger.info('ENTRY')
	start = config.EMIL_CONTENT.HTML_HEADER
	end =   config.EMIL_CONTENT.HTML_FOOTER
	formated = content
	send_from='<p style="color:#FFAA00"><b>' + email_source+ '</b></p>'
	for item in pnp_posts:
		formated += '<br>'
		formated += '<b>' + item['timeStamp'] + '</b>'
		formated += '<br>'
		for i in item['content']:
			formated += '<p>' + i + '</p>'
			formated += '<br>'
		formated += '<br><br>'
	whole = start+formated+send_from+end
	logger.debug('format_post() %s', whole[-9:])
	logger.info('EXIT')
	return whole.encode('utf-8')

def create_time_check_string():
	"""
	Get EST time and a time string without format
	Input:
	Return: time_check(datetime), str(string)
	"""
	#utc to ESTs
	time_check = dt.datetime.utcnow() - dt.timedelta(0, 4*3600) #utc to ESTs
	return time_check, str(time_check.year)+str(time_check.month) + str(time_check.day) + str(time_check.hour)

def daily_check(pnp_posts, email_source):
	"""
	Send email at 8am and 5pm per day to indicate the program is running fine
	Input: pnp_posts(list of dict), email_source(string)
	Return: Boolean
	"""	
	logger.info('ENTRY')
	time_check, d_short_msg = create_time_check_string()
	if time_check.hour == 17 or time_check.hour == 8:
		content = config.EMIL_CONTENT.END_OF_DAY_CONTENT
		d_msg = format_post(pnp_posts, content, email_source)
		if (d_short_msg in past_posts.keys()) == False:
			past_posts[d_short_msg] = d_short_msg
			if _send_email(d_msg, title= config.EMIL_CONTENT.END_OF_DAY_TITLE):
				return True
	logger.debug('is_new_email() check hour:%s',time_check)
	logger.info('EXIT')
	return False


def is_new_post(past_posts, pnp_posts):
	"""
	read the pnp_posts.content to see if it's in the past_posts if not, add the post to the need to send email list
	Input: past_posts(dict), pnp_posts(list of dict)
	Return: need_to_send(list)
	"""
	need_to_send = []
	#read the past posts from the JSON file location
	past_posts = read_from_traget(json_file)
	if pnp_posts:
		for item in pnp_posts:
			msg = '%'.join([i for i in item['content']]).replace(' ','').lower()
			shorten_msg = [msg[i] for i in range(len(msg)) if i % 3 == 0]
			shorten_msg = ''.join(shorten_msg)
			if (shorten_msg in past_posts.keys()) == False:
				past_posts[shorten_msg] = item['timeStamp']
				need_to_send.append(item)
	return need_to_send

def is_new_email(pnp_posts, json_file, email_source):
	"""
	read the past posts from the JSON file location and compare with the current posts to decide if send an email
	also, send daily check email at 8am and 5pm
	Input: pnp_posts(list of dict), json_file(string), email_source(string)
	"""
	logger.info('ENTRY')
	
	#read the past posts from the JSON file location
	past_posts = read_from_traget(json_file)
	need_to_send = is_new_post(past_posts, pnp_posts)
	if need_to_send:
		out_html = format_post(need_to_send, ' ' , email_source)
		if _send_email(out_html):
			logger.info('EXIT', out_html[-30:])
			return True
	else:
		daily_check(pnp_posts, email_source)
	save_dict_to_json(past_posts, json_file)
	logger.info('EXIT')


def _main():
	"""
	Get past posts and send out email by calling is_new_email()
	Input:
	Return: Boolean, if send, True
	"""
	time_check, _ = create_time_check_string()
	logger.debug('email_handler_main() Run time is EST:%s', time_check.strftime(config.LOG_CONFIG.datefmt))
	logger.info('ENTEY')
	json_file = config.OUTPUT.past_posts
	time_mark = get_time_mark()
	pnp_posts = parse_pnp_posts(time_mark)

	if len(pnp_posts):
		logger.debug('email_handler_main() Posts: '+ ' '.join(pnp_posts[0]['content']))
		email_machine_name = platform.uname()[1]
		is_new_email(pnp_posts, json_file, email_machine_name)
		logger.debug('email_handler_main() Posts: %s', pnp_posts[-20:])
		logger.info('EXIT')
		return True
	else:
		logger.debug('email_handler_main() Posts: []')
		logger.info('EXIT')
		return False
		

if __name__ == '__main__':
	time_check = dt.datetime.utcnow() - dt.timedelta(0, 4*3600)
	print 'EST: ', time_check.strftime(config.LOG_CONFIG.datefmt) 
	_main()



