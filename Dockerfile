FROM ubuntu:latest

# Install python and pip
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    build-essential \
    ca-certificates \
    gcc \
    git \
    libpq-dev \
    make \
    python-pip \
    python2.7 \
    python2.7-dev \
    ssh \
    xvfb \
    firefox \
    vim \
    cron \
    && apt-get autoremove \
    && apt-get clean
RUN pip install -U setuptools
RUN pip install selenium
RUN pip install pyvirtualdisplay
RUN pip install bs4

ADD /home/pnpCrawler /opt/pnpCrawler

#COPY crontab /etc/cron.d/cool-task
#RUN chmod 0644 /etc/cron.d/cool-task

#RUN (crontab -l ; echo "TZ=America/Toronto")| crontab -
RUN (crontab -l ; echo "0 */2 * * * /opt/pnpCrawler/src/clear_log.sh")| crontab -
RUN (crontab -l ; echo "* * * * * cd /opt/pnpCrawler/src && python email_handler.py")| crontab -


#CMD tail -f /dev/null #this line will make the container keeps running
#CMD [ "python", "/opt/pnpAtPythonanywhere/src/email_handler.py" ]

ENTRYPOINT service cron start && /bin/bash
