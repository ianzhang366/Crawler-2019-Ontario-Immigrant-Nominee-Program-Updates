# A Crwaler for 2019 Ontario Immigrant Nominee Program Updates page
## Project Idea
This project is a small crwaler, which will parse info from the [2019 Ontario Immigrant Nominee Program Updates](https://www.ontario.ca/page/2019-ontario-immigrant-nominee-program-updates) page every 30 seconds, if there's new update it will send email to the recipents.

## Project Structure
To achieve the goal, I used the python to parse the site and sending out emails, using the beautiful soup, selenium and smtplib. To simplifiy the deploy process, I built up an docker image for this project. Within the image, I used crontab job to run the project every 30 seconds.

### Project structure tree
```
../pnpCrawler
|-- src
|   |-- perform_execute.py
|   |-- log_control.py
|   |-- json_handler.py
|   |-- helper.py
|   |-- geckodriver.log
|   |-- data_logic.py
|   |-- config.example
|   |-- clear_log.sh
|   |-- _past_posts.json
|   |-- _email_send_handler.py
|   |-- _config.py
|   `-- ToDo.txt
|-- setup.sh
|-- pnpCrawlerData
|   |-- output
|   |   |-- past_posts.json
|   |   `-- log_daily.log
|   |-- geckodriver
|   `-- config.py
|-- one_shot_docker.sh
|-- README.md
`-- Dockerfile
```
jupyter notebook password create the encrypted password string at the following file, 
../.jupyter/jupyter_notebook_config.json

When rebuild the images, ensure delete the old one, otherwise mid-image will get generated.

The main function is perform_execute.py, which will call the data_logic.py to get the updates from the target website. 

The log is stroed at the ../pnpCrawlerData/output, past_posts.json is used to store the past update, which help us avoid sending all the updates from the target page every time.

Also, I put the configuration at the config.py which is not visiable on github due to email info, but I provided the _config.py as example for it, you can use it to get your own version. 

_past_posts.json is an storage example of the past update.

In addition, the Dockerfile is presented, you can modify it to get your own image.

### Notes of Dockerfile
Crontab job, ```30 * * * * cd /tmp && rm -r ./*```, this one is added to avoid the temp file of geckodriver taking over all the space.
