from selenium import webdriver
from pyvirtualdisplay import Display
import time

import _config

import sys
sys.path.append(_config.SEN_CONFIG.data_location)

import config
from log_control import log_main

logger = log_main('log_pnp_getSourcePage')


def get_updates_page(target_site):
	"""
	Get the raw_html of first page at the target_site
	Input: target_site(string), an URL
	Output: raw_html(string)
	"""
	path_to_exe = config.GECKODRIVER.path_to_exe
	logger.info('ENTRY')
	logger.debug('get_updates_page()  target_site, driver path: ' + target_site + ', '+ path_to_exe )
	with Display():
		try:
			driver = webdriver.Firefox(executable_path=path_to_exe)
			driver.get(target_site)
			raw_html = driver.page_source.encode('utf-8')
			time.sleep(2)
			if len(raw_html) <= 130:
				logger.debug('get_updates_page() %s',raw_html)
				logger.info('Exit')
			else:
				logger.debug('get_updates_page() %s',raw_html[0:100])
				logger.info('Exit')

			return raw_html
		except Exception as err:
			logger.info(err)


if __name__ == '__main__':
	target_site = 'http://www.ontarioimmigration.ca/en/pnp/OI_PNPNEW.html'
	info_page = get_updates_page(target_site)
	print type(info_page), info_page
