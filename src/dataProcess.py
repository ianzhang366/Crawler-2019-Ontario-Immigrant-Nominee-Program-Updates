from bs4 import BeautifulSoup
import time, re
from collections import defaultdict
# from main import time_convert
# from log_control_dp import log_data_process
from log_control import log_main

logger = log_main('log_pnp_dataProcess')

######################### Logging ##########################
# logger = log_data_process()

def time_convert(time_string):
	# logger.debug('ENTRY: time_convert() time_string: '+ time_string)
	tmp = time_string.replace('u', '')
	tmp = time_string.replace(',', '')
	tmp = tmp.replace('th', '')
	try:
		time_mark = time.strptime(tmp, "%b %d %Y")
		return time_mark
	except Exception as err:
		time_mark = time.strptime(tmp, "%B %d %Y")
		return time_mark

def get_related_post(posts, last_timestamp):
	# posts is dict
	logger.info('ENTRY: filter_by_time()')
	time_filter_posts = []
	for key, value in posts.items():
		# print last_timestamp, value['timeStamp']
		if (last_timestamp < time_convert(value['timeStamp'])):
			logger.info(str(last_timestamp)+', '+str(value['timeStamp']))
			time_filter_posts.append(posts[key])
				# print value['timeStamp']
	logger.info('EXIT: filter_by_time() %s', posts.keys())
	return time_filter_posts


def create_post_dict(data): # this class will get all the posts at the update site first page, which means it can't be none
	# data is list
	logger.info('ENTRY: create_post_dict()')
	if data == False:
		return {}
	post = defaultdict()
	time_p = re.compile(r"""^[A-Z].*\d{4}$""") #.*d{2}+,d{4}
	num = 1
	cnt = 0
	for line in data:
		if time_p.search(line):
			# print "time matched: ", line
			post[num] = {'timeStamp': line, 'content': []}
			cnt = num
			num += 1
		else:
			if cnt:
				post[cnt]['content'].append(line)
	logger.info('EXIT: create_post_dict() %s', post.keys())
	return post

######################### Parse content from html ##########################
def parse_content(page_info, target_element, keyword):
	#page_info is raw html
	logger.info('ENTRY: parse_content() keyword: ' + keyword)
	# print type(page_info), page_info
	try:
		soup = BeautifulSoup(page_info, "html.parser")
		data = []
		posts = soup.findAll('div', {"class": target_element})
		for tag in posts:
			post_contents = tag.find_all("p")
			# print type(post_content), post_content
			for post in post_contents:
				data.append(post.text)
		if data == []:
			logger.info('Exit: parse_content() %s', data)
			return False
		logger.info('Exit: parse_content() %s', data[0])
		return create_post_dict(data)
	except Exception as err:
		# print 'dataProcess: ', err
		logger.exception(err)


if __name__ == '__main__':
	string = ['January 26, 2018', 'Re: OINP now accepting applications to the Masters Graduate and PhD Graduate Streams']
	print create_post_dict(string)
