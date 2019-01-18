"""
Set up the external configuration path
"""
PATH_ = '../pnpCrawlerData'

class SENT_EMAIL:
    gmail_user=''
    gmail_pwd=''
    recipient=['emailAddress', 'emailAddress']

class LOG_CONFIG:
    import logging
    location= PATH_ + '/output/log_daily.log'
    content_formate='%(asctime)s.%(msecs)03d:%(levelname)s:%(module)s:%(funcName)s:%(lineno)d:%(message)s'
    datefmt='%Y-%m-%d %H:%M:%S'
    log_base_level= logging.DEBUG
    log_to_file= logging.INFO
    print_console=True


class CRWALER_PARA:
    target_site='https://www.ontario.ca/page/2019-ontario-immigrant-nominee-program-updates'
    targetElement='pagebody'
    keyword='Masters Graduate'

class GECKODRIVER:
    path_to_exe= PATH_ + '/geckodriver'

class OUTPUT:
    past_posts= PATH_ + '/output/past_posts.json'

class EMAIL_CONTENT:
    TIMT_FORMAT="%Y-%m-%d"
    HTML_HEADER='<html><head></head><body>'
    HTML_FOOTER='</body></html>'
    PARSE_FUNC_FAIL_CONTENT= "<b>It seems the parse function of the updates page is not running correctly.</b>"
    DEBUG_EMAIL_TITLE='Updates Debug Email'
    BEGIN_OF_DAY_TITLE="PNP robot: Master, I'm about to start the day, hopefully you will have a great day!"
    BEGIN_OF_DAY_CONTENT="<b>A brand new day, let's see what will happen!</b>"
    END_OF_DAY_TITLE="PNP robot: I'm done for the day!"
    END_OF_DAY_CONTENT="Nothing happened during the day, will keep an eye during the night."
    CONTENT="<b>We don't have any updates today till the office hour done. But I will keep working during the night!</b>"
