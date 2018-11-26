from bs4 import BeautifulSoup
import time, re
from collections import defaultdict

from log_control import log_main

logger = log_main('log_pnp_dataProcess')


def time_convert(time_string):
	"""
	A utility function, convert string to datetime
	Input: time_string(string)
	Return: time_mark(datetime)
	"""
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
	"""
	Filter the parsed result after last_timestamp
	Input: posts(list), last_timestamp(string)
	Return: time_filter_posts(list of dict)
	"""
	# posts is dict
	logger.info('ENTRY')
	time_filter_posts = []
	for key, value in posts.items():
		# print last_timestamp, value['timeStamp']
		if (last_timestamp < time_convert(value['timeStamp'])):
			logger.debug(str(last_timestamp)+', '+str(value['timeStamp']))
			time_filter_posts.append(posts[key])
				# print value['timeStamp']
	logger.debug('filter_by_time() %s', posts.keys())
	logger.info('EXIT')
	return time_filter_posts


def create_post_dict(data): 
	"""
	Get all the posts at the first page of the target site , which can't be none
	Input: data(list)
	Return: post(dict) 
		{count: 
			{	post_content:[], 
				timeStamp:[string] 
			}
		}
	"""
	# data is list
	logger.info('ENTRY')
	if data == False:
		return {}
	post = defaultdict()
	#find time stamp pattern within lines, eg: .*d{2}+,d{4}
	time_p = re.compile(r"""^[A-Z].*\d{4}$""") 
	num = 1
	cnt = 0
	for line in data:
		 #building the post by reading the timeStamp stream
		 #1990-10-1
		 #line a
		 #line b
		 #1990-10-2
		 #line c
		 #line d
		if time_p.search(line):
			# print "time matched: ", line
			post[num] = {'timeStamp': line, 'content': []}
			cnt = num
			num += 1
		else:
			if cnt:
				post[cnt]['content'].append(line)
	logger.debug('create_post_dict() %s', post.keys())
	logger.info('EXIT')
	return post

def parse_content(raw_html, target_element, keyword):
	"""
	Get all the posts at the first page of the target site , which can't be none
	Input: raw_html(string), target_element(string), keyword(string)
	Return: data(list)
	"""
	#raw_html is raw html
	logger.info('ENTRY')
	# print type(raw_html), raw_html
	try:
		soup = BeautifulSoup(raw_html, "html.parser")
		data = []
		posts = soup.findAll('div', {"class": target_element})
		for tag in posts:
			post_contents = tag.find_all("p")
			# print type(post_content), post_content
			for post in post_contents:
				data.append(post.text)
		if data == []:
			logger.debug('parse_content() %s', data)
			logger.info('Exit')
			return False
		logger.debug('parse_content() %s', data[0])
		logger.info('Exit')
		return create_post_dict(data)
	except Exception as err:
		# print 'dataProcess: ', err
		logger.exception(err)


if __name__ == '__main__':
	string = ['January 26, 2018', 'Re: OINP now accepting applications to the Masters Graduate and PhD Graduate Streams']
	print create_post_dict(string)
