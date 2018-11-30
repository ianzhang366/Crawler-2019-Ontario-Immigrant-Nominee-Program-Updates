"""
# send email if:
# a, new post detected comparing with the past post
# b, daily check emails
"""
import sys
import time
import platform

import datetime as dt

from data_logic import parse_pnp_posts

from json_handler import save_dict_to_json, read_from_traget
from _email_send_handler import _send_email
from helper import create_time_check_string, get_time_marker

from log_control import log_main
import _config
import config

sys.path.append(_config.SEN_CONFIG.data_location)

LOGGER = log_main('log_pnp_email_handler')
JSON_FILE = config.OUTPUT.past_posts

def format_post(pnp_posts, content, email_source):
    """
    Put up a HTML string
    Input: pnp_posts(list of dict), content(string, predefined email content),
        email_source(string) where the email is from
    Return: whole(string, HTML)
    """
    LOGGER.info('ENTRY')
    start = config.EMAIL_CONTENT.HTML_HEADER
    end = config.EMAIL_CONTENT.HTML_FOOTER
    formated = content
    send_from = '<p style="color:#FFAA00"><b>' + email_source+ '</b></p>'
    if pnp_posts:
        for item in pnp_posts:
            formated += '<br>'
            formated += '<b>' + item['timeStamp'] + '</b>'
            formated += '<br>'
            for i in item['content']:
                formated += '<p>' + i + '</p>'
                formated += '<br>'
            formated += '<br><br>'
    whole = start+formated+send_from+end
    LOGGER.debug('format_post() %s', whole[-9:])
    LOGGER.info('EXIT')
    return whole.encode('utf-8')


def daily_check(pnp_posts, email_source):
    """
    Send email at 8am and 5pm per day to indicate the program is running fine
    Input: pnp_posts(list of dict), email_source(string)
    Return: Boolean
    """	
    LOGGER.info('ENTRY')
    #use the time stamp to mark the daily job to the past post file
    time_check, d_short_msg = create_time_check_string()
    save_flag = 0
    past_posts = read_from_traget(JSON_FILE)
    if time_check.hour == 17 or time_check.hour == 8:
        if time_check.hour == 17:
            content = config.EMAIL_CONTENT.END_OF_DAY_CONTENT
            title = config.EMAIL_CONTENT.END_OF_DAY_TITLE
        else:
            content = config.EMAIL_CONTENT.BEGIN_OF_DAY_CONTENT
            title = config.EMAIL_CONTENT.BEGIN_OF_DAY_TITLE
        
        d_msg = format_post(pnp_posts, content, email_source)
        if (d_short_msg in past_posts.keys()) == False:
            save_flag = True
            past_posts[d_short_msg] = d_short_msg
            if _send_email(d_msg, title=title):
                return True
    if save_flag:
        save_dict_to_json(past_posts, JSON_FILE)
    LOGGER.debug('is_new_email() check hour:%s', time_check)
    LOGGER.info('EXIT')
    return False


def is_new_post(past_posts, cur_posts):
    """
    read the pnp_posts.content to see if it's in the past_posts if not, add the 
    post to the need to send email list
    Input: past_posts(dict), pnp_posts(list of dict)
    Return: need_to_send(list)
    # cur_posts =
    # [
    #     {
    #         post_content:[], 
    #         timeStamp:[string]
    #     },
    # ]

    past_post={
        shorten_msg:timeStamp[string] 
        }
    """
    LOGGER.info('ENTRY')
    need_to_send = []
    save_flag = False
    #read the past posts from the JSON file location
    if cur_posts:
        for item in cur_posts:
            #here we used the content to generate a key for past_post dictionary
            #in this way we can minimize the storage of past_post
            msg = '%'.join([i for i in item['post_content']]).replace(' ', '').lower()
            shorten_msg = [msg[i] for i in range(len(msg)) if i % 6 == 0]
            shorten_msg = ''.join(shorten_msg)
            if (shorten_msg in past_posts.keys()) == False:
                save_flag = True
                past_posts[shorten_msg] = item['timeStamp']
                need_to_send.append(item)
    if save_flag:
        save_dict_to_json(past_posts, JSON_FILE)
        return [' \t'.join(str(i)) for i in need_to_send][0]
    LOGGER.debug('need_to_send',need_to_send)
    LOGGER.info('EXIT')
    return []

def is_new_email(cur_posts, JSON_FILE, email_source):
    """
    read the past posts from the JSON file location and compare with the current posts to 
    decide if send an email also, send daily check email at 8am and 5pm
    Input: pnp_posts(list of dict), JSON_FILE(string), email_source(string)
    # cur_posts =     
    # [
    #     {
    #         post_content:[], 
    #         timeStamp:[string]
    #     },
    # ]
    """
    LOGGER.info('ENTRY')
    #read the past posts from the JSON file location
    past_posts = read_from_traget(JSON_FILE)
    need_to_send = is_new_post(past_posts, cur_posts)
    if need_to_send:
        out_html = format_post(need_to_send, ' ', email_source)
        if _send_email(out_html):
            LOGGER.debug('out_html', out_html[-30:])
            LOGGER.info('EXIT')
            return True
    daily_check(cur_posts, email_source)
    return False
    LOGGER.info('EXIT')

def _main():
    """
    Get past posts and send out email by calling is_new_email()
    Input:
    Return: Boolean, if send, True
    """
    LOGGER.info('ENTEY')
    time_check, _ = create_time_check_string()
    LOGGER.debug('Run time is EST:%s', time_check.strftime(config.LOG_CONFIG.datefmt))
    JSON_FILE = config.OUTPUT.past_posts
    time_marker = get_time_marker()
    #past 5 days
    # __posts =     
    # [
    #     {
    #         post_content:[], 
    #         timeStamp:[string]
    #     },
    # ]
    cur_posts = parse_pnp_posts(time_marker)

    if cur_posts:
        LOGGER.debug('email_handler_main() Posts: '+ ' '.join(cur_posts[0]['post_content']))
        email_machine_name = platform.uname()[1]
        is_new_email(cur_posts, JSON_FILE, email_machine_name)
        LOGGER.debug('email_handler_main() Posts: %s', cur_posts[-20:])
        LOGGER.info('EXIT')
        return True
    return False

if __name__ == '__main__':
    time_check = dt.datetime.utcnow() - dt.timedelta(0, 4*3600)
    print 'EST: ', time_check.strftime(config.LOG_CONFIG.datefmt) 
    _main()



