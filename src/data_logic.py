"""
parse_pnp_posts(time_marker)
parse the post of past time_marker:days
raw_html = get_updates_page(target_site)
posts = parse_content(raw_html, targetElement, keyword)
if not post is pased then send out an emial to indicate the issue
"""
import sys
import time
import re

from datetime import timedelta
from datetime import datetime as dt
from collections import defaultdict

from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display

from log_control import log_main
from _email_send_handler import _send_email
from helper import time_convert, get_time_marker

import _config
import config

sys.path.append(_config.SEN_CONFIG.data_location)

LOGGER = log_main('log_pnp_data_logic')
TIMT_FORMAT = "%Y-%m-%d"

def create_post_dict(data): 
    """
    Get all the posts at the first page of the target site , which can't be none
    Input: data(list)
    Return: post(dict) 
            {	
                timeStamp:post_content
            }
    """
    # data is list
    LOGGER.info('ENTRY')
    if data:
        post = defaultdict()
        #find time stamp pattern within lines, eg: .*d{2}+,d{4}
        time_p = re.compile(r"""^[A-Z].*\d{4}$""") 
        flag = 0
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
                time_stamp = line
                post[time_stamp] = []
                flag = 1
                #post[num] = {'timeStamp': line, 'post_content': []}
                #cnt = num
                #num += 1
            #else:
                #if cnt:
                 #   post[cnt]['post_content'].append(line)
            if flag:
                post[time_stamp].append(line)
        LOGGER.debug('create_post_dict() %s', post.keys())
        LOGGER.info('EXIT')
        return post
    else:
        return {}

def pasered_zero_send_email():
    """
    handles exception, when the parser can't get info at all, normally it should get the past 5days posts.
    """
    LOGGER.info('ENTRY')
    try:
        start = config.EMAIL_CONTENT.HTML_HEADER
        end = config.EMAIL_CONTENT.HTML_FOOTER
        formated = config.EMAIL_CONTENT.PARSE_FUNC_FAIL_CONTENT
        _send_email(start+formated+end, config.EMAIL_CONTENT.DEBUG_EMAIL_TITLE)
        LOGGER.info('EXIT')
    except Exception as err:
        LOGGER.exception(err)
        LOGGER.info('EXIT')

def parse_content(raw_html, target_element, keyword):
    """
    Get all the posts at the first page of the target site , which can't be none
    Input: raw_html(string), target_element(string), keyword(string)
    Return: posts[], which contains the whole html page, top to bottom in string
    eg:
        timeStamp:#1990-10-1
            post_content:[#line a, #line b]
    """
    #raw_html is raw html
    LOGGER.info('ENTRY')
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
        if data:
            LOGGER.debug('parse_content() %s', data[0])
            LOGGER.info('Exit')
            return create_post_dict(data)
        LOGGER.debug('parse_content() %s', data)
        LOGGER.info('Exit')
        return False
    except Exception as err:
        # print 'dataProcess: ', err
        LOGGER.exception(err)
        return False

def get_related_post(posts, last_timestamp):
    """
    Filter the parsed result after last_timestamp
    # posts[], which includes the html page string, from top to botton
    # Input: posts(list), last_timestamp(string)
    # Return: time_filter_posts(list of dict)
    # [
    #     {
    #         timeStamp:[string]
    #     },
    # ]
    """
    # posts is dict
    LOGGER.info('ENTRY')
    time_filter_posts = []
    #basiclly, first, we flat the dict, posts, to value{{post_content:[], timeStamp:[string]}}
    #second, we convert the timestamp at the flated dict, value, to datetime stamp
    #third, we filter out the content by the time condition
    for post in posts.items():
        # print last_timestamp, value['timeStamp']
       # print 'input: %s', last_timestamp, 't %s', time_convert(value['timeStamp'])
        if (last_timestamp < time_convert(post[0])):
            LOGGER.debug(str(last_timestamp)+', '+post[0])
            time_filter_posts.append(post)
                # print value['timeStamp']
    LOGGER.debug('filter_by_time() %s', posts.keys())
    LOGGER.info('EXIT')
    return time_filter_posts

def get_updates_page(target_site):
    """
    Get the raw_html of first page at the target_site
    Input: target_site(string), an URL
    Output: raw_html(string) ''
    """
    path_to_exe = config.GECKODRIVER.path_to_exe
    LOGGER.info('ENTRY')
    LOGGER.debug('get_updates_page()  target_site, driver path: ' + target_site + ', '+ path_to_exe )
    with Display():
        try:
            driver = webdriver.Firefox(executable_path=path_to_exe)
            driver.get(target_site)
            raw_html = driver.page_source.encode('utf-8')
            time.sleep(2)
            if len(raw_html) <= 130:
                LOGGER.debug('get_updates_page() %s',raw_html)
                LOGGER.info('Exit')
            else:
                LOGGER.debug('get_updates_page() %s',raw_html[0:100])
                LOGGER.info('Exit')
            return raw_html
        except Exception as err:
            LOGGER.debug(err)

def parse_pnp_posts(time_marker):
    """
    Pasrse the target page and get past_days' post

    Input: time_marker(int)
    Return: past_posts(list)
    """
    LOGGER.info('ENTRY')
    LOGGER.debug('parse_pnp_posts() time_marker: '+ str(time_marker))
    #set up initialzation figures
    target_site = config.CRWALER_PARA.target_site
    # div by class name
    targetElement = config.CRWALER_PARA.targetElement 
    #get the raw html
    raw_html = get_updates_page(target_site) 
    if raw_html:
        keyword = config.CRWALER_PARA.keyword
        try:
            #parse parse defined by raw_html, targetElement, keyword
            # posts(dict) 
            # {count: # count itself is used to collapse the content by timestap
            #     {	post_content:[], 
            #         timeStamp:[string] 
            #     }
            # }
            posts = parse_content(raw_html, targetElement, keyword)
            # if we get 0 posts, send email to indicate that the parse function is broken
            if posts.keys():
                    
                #filter the parsed result by date, time_marker
                #past_posts =     
                # [
                #     {
                #         post_content:[], 
                #         timeStamp:[string]
                #     },
                # ]
                past_posts = get_related_post(posts, time_marker)
                if past_posts:
                    LOGGER.debug(' parse_pnp_posts() %s', past_posts[0])
                    LOGGER.info('EXIT')
                return past_posts
            pasered_zero_send_email()
            LOGGER.info('EXIT')
            return []
        except Exception as err:
            LOGGER.exception(err)
            return []
    else:
        LOGGER.info('EXIT')
        return []


######################### Handle Main logic ##########################
if __name__ == '__main__':
    LOGGER.info('ENTRY: data_logic() as MAIN')
    time_marker = get_time_marker()
    print parse_pnp_posts(time_marker)
    LOGGER.info('EXIT: data_logic() as MAIN')

