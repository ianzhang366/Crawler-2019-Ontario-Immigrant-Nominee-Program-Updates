class SENT_EMAIL:
    gmail_user='ian.zhang366@gmail.com'
    gmail_pwd='p@ss4Goog'
    recipient=['ian.zhang366@gmail.com', 'lisa411854746@gmail.com']

class LOG_CONFIG:
    import logging
    location='../pnpCrawlerData/output/log_daily.log'
    content_formate='%(asctime)s.%(msecs)03d:%(levelname)s:%(module)s:%(funcName)s:%(lineno)d:%(message)s'
    datefmt='%Y-%m-%d %H:%M:%S'
    log_base_level= logging.DEBUG
    log_to_file= logging.INFO
    print_console=False
    past_posts='./pnpCrawlerData/output/past_posts.json'


class CRWALER_PARA:
    target_site='http://www.ontarioimmigration.ca/en/pnp/OI_PNPNEW.html'
    targetElement='main_content'
    keyword='Masters Graduate'

class GECKODRIVER:
    path_to_exe='../pnpCrawlerData/geckodriver'

class OUTPUT:
    past_posts='../pnpCrawlerData/output/past_posts.json'

