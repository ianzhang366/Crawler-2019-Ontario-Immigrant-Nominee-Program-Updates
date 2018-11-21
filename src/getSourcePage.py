from selenium import webdriver
from pyvirtualdisplay import Display
import time
import os,sys
from log_control import log_main

logger = log_main('log_pnp_getSourcePage')
os.chdir(sys.path[0])
# from log_control_dp import log_get_pagesource

######################### Logging ##########################
# logger = log_get_pagesource()

def get_updates_page(target_site):
	path_to_exe = os.path.abspath('.') + '/geckodriver'
	logger.info('ENTRY: get_updates_page() target_site: ' + target_site)
	logger.info('ENTRY: get_updates_page() driver path: ' + path_to_exe)
	with Display():
		try:
			driver = webdriver.Firefox(executable_path=path_to_exe)
			driver.get(target_site)
			page_info = driver.page_source.encode('utf-8')
# 			print 'in display', page_info
			time.sleep(2)
			# print type(page_info)
			# tmp = ''.join([page_info[i] for i in range(len(page_info)) if i % 111 == 0])
			if len(page_info) <= 130:
				logger.info('Exit: get_updates_page() %s',page_info)
			else:
				logger.info('Exit: get_updates_page() %s',page_info[0:100])
			return page_info
		except Exception as err:
			logger.info(err)
#		finally:

# 			driver.quit()

if __name__ == '__main__':
	target_site = 'http://www.ontarioimmigration.ca/en/pnp/OI_PNPNEW.html'
	targetElement = 'right_column' # div by class name
	keyword = 'master stream'
	info_page = get_updates_page(target_site)
	print type(info_page), info_page
