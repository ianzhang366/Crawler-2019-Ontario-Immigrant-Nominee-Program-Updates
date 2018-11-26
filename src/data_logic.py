import time
from datetime import timedelta
from datetime import datetime as dt
from getSourcePage import get_updates_page
from dataProcess import parse_content, get_related_post
from log_control import log_main
from _email_send_handler import _send_email

import _config

import sys

sys.path.append(_config.SEN_CONFIG.data_location)

import config

logger = log_main('log_pnp_data_logic')

TIMT_FORMAT="%Y-%m-%d"


def get_time_mark(past_days=-5):
	"""
	Get datetime of last 5 days
	Input: past_days(int)
	Return: (datetime)
	"""
	logger.info('ENTRY')
	logger.debug('ENTRY: get_time_mark() past_days = ' + str(past_days))

	date = dt.today().date()
	date += timedelta(past_days) # this variable determine how many day do we check backward for the updates
	logger.debug('get_time_mark() %s', str(time.strptime(str(date), TIMT_FORMAT)))
	logger.info('EXIT')
	return time.strptime(str(date), TIMT_FORMAT)

def parse_pnp_posts(time_mark):
	"""
	Pasrse the target page and get past_days' post
	Input: time_mark(int)
	Return: past_posts(list)
	"""
	logger.info('ENTRY')
	logger.debug('parse_pnp_posts() time_mark: '+ str(time_mark))
	#set up initialzation figures
	target_site = config.CRWALER_PARA.target_site
	targetElement = config.CRWALER_PARA.targetElement # div by class name
	raw_html = get_updates_page(target_site)

	if raw_html:
		keyword = config.CRWALER_PARA.keyword
		try:
			#parse parse defined by raw_html, targetElement, keyword
			posts = parse_content(raw_html, targetElement, keyword)
			# if we get 0 posts, send email to indicate that the parse function is broken
			if len(posts.keys()) == 0:
				start = config.EMIL_CONTENT.HTML_HEADER
				end =  config.EMIL_CONTENT.HTML_FOOTER
				formated = config.EMIL_CONTENT.PARSE_FUNC_FAIL_CONTENT
				_send_email(start+formated+end, config.EMIL_CONTENT.DEBUG_EMAIL_TITLE)
			#filter the parsed result by date, time_mark
			past_posts = get_related_post(posts, time_mark)
			if past_posts:
				logger.debug(' parse_pnp_posts() %s', past_posts[0])
				logger.info('EXIT')
			else:
				logger.debug('parse_pnp_posts() []', )
				logger.info('EXIT')
			return past_posts
		except Exception as err:
			logger.exception(err)
	else:
		logger.info('EXIT')
		return []


######################### Handle Main logic ##########################
if __name__ == '__main__':
	logger.info('ENTRY: data_logic() as MAIN')
	time_mark = get_time_mark()
	print parse_pnp_posts(time_mark)
	logger.info('EXIT: data_logic() as MAIN')

