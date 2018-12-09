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
    python3-pip \
    && apt-get autoremove \
    && apt-get clean 
RUN pip install -U setuptools
RUN pip install selenium
RUN pip install pyvirtualdisplay
RUN pip install bs4
RUN pip install jupyter
RUN pip install jupyter_contrib_nbextensions
RUN jupyter nbextensions_configurator enable --system
RUN jupyter nbextension enable codefolding/main
RUN pip3 install ipython[all]
#RUN jupyter notebook --generate-config
#adding the project to image
ADD . /opt/pnpCrawler
ADD jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py 


#COPY crontab /etc/cron.d/cool-task
#RUN chmod 0644 /etc/cron.d/cool-task

#RUN (crontab -l ; echo "TZ=America/Toronto")| crontab -
RUN (crontab -l ; echo "30 * * * * cd /opt/pnpCrawler/src && ./clear_log.sh")| crontab -
RUN (crontab -l ; echo "* * * * * cd /opt/pnpCrawler/src && python perform_execute.py")| crontab -


#CMD tail -f /dev/null #this line will make the container keeps running
#CMD [ "python", "/opt/pnpAtPythonanywhere/src/email_handler.py" ]

ENTRYPOINT service cron start && cd /opt/pnpCrawler/src && jupyter notebook --ip=0.0.0.0 --allow-root
#ENTRYPOINT service cron start && /bin/bash

