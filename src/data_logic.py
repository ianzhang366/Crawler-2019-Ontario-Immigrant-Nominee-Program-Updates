import time
from datetime import timedelta
from datetime import datetime as dt
from getSourcePage import get_updates_page
from dataProcess import parse_content, get_related_post
from log_control import log_main
from _email_send_handler import _send_email

import sys
sys.path.append('../pnpCrawlerData')
import config

logger = log_main('log_pnp_data_logic')

def get_time_mark(past_days=-5):
	logger.info('ENTRY: get_time_mark() past_days = ' + str(past_days))
	date = dt.today().date()
	date += timedelta(past_days) # this variable determine how many day do we check backward for the updates
	logger.info('EXIT: get_time_mark() %s', str(time.strptime(str(date), "%Y-%m-%d")))
	return time.strptime(str(date), "%Y-%m-%d")

def parse_pnp_posts(time_mark):
	logger.info('ENTRY: parse_pnp_posts() time_mark: '+ str(time_mark))
	#set up initialzation figures
	target_site = config.CRWALER_PARA.target_site
	targetElement = config.CRWALER_PARA.targetElement # div by class name
	raw_element = get_updates_page(target_site)

	if raw_element:
		keyword = config.CRWALER_PARA.keyword
		try:
			posts = parse_content(raw_element, targetElement, keyword)
# 			print posts
			if len(posts.keys()) == 0: # if we get 0 posts then it means the parse function is broken
				start = '<html><head></head><body>'
				end =   '</body></html>'
				formated ="<b>It seems the parse function of the updates page is not running correctly.</b>"
				_send_email(start+formated+end, 'Updates Debug Email')
			start_posts = get_related_post(posts, time_mark)
			if start_posts:
				logger.info('EXIT: parse_pnp_posts() %s', start_posts[0])
			else:
				logger.info('EXIT: parse_pnp_posts() []', )
			return start_posts
		except Exception as err:
			logger.exception(err)
			# print 'parse_pnp_posts: ', err
			# logger_debug.exception(err)
	else:
		logger.info('EXIT: parse_pnp_posts() False')
		return False


######################### Handle Main logic ##########################
if __name__ == '__main__':
	logger.info('ENTRY: data_logic() as MAIN')
	time_mark = get_time_mark()
	print parse_pnp_posts(time_mark)
	logger.info('EXIT: data_logic() as MAIN')

