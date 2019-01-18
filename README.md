# A Crwaler for 2019 Ontario Immigrant Nominee Program Updates page
## Project Idea
This project is a small crwaler, which will parse info from the 2019 Ontario Immigrant Nominee Program Updates(https://www.ontario.ca/page/2019-ontario-immigrant-nominee-program-updates) page.

More specificly, it will parse the page every 30 seconds, if there's new update it will send email to the recipents.

## Project Structure
To achieve the goal, I used the python to parse the site and sending out emails, using the beautiful soup, selenium and smtplib. To simplifiy the deploy process, I built up an docker image for this project. Within the image, I used crontab to run the project every 30 seconds.

### Project structure tree
```
../pnpCrawler
├── src
│   ├── perform_execute.py
│   ├── log_control.py
│   ├── json_handler.py
│   ├── helper.py
│   ├── geckodriver.log
│   ├── data_logic.py
│   ├── config.example
│   ├── clear_log.sh
│   ├── _email_send_handler.py
│   ├── _config.py
│   └── ToDo.txt
├── setup.sh
├── pnpCrawlerData
│   ├── output
│   │   ├── past_posts.json
│   │   └── log_daily.log
│   ├── geckodriver
│   └── config.py
├── one_shot_docker.sh
├── README.md
└── Dockerfile
```

The main function is perform_execute.py, which will call the data_logic.py to get the updates from the target website. The log is stroed at the ../pnpCrawlerData/output.
Also, I put the configuration at the config.py which is not visiable on github, but I provided the _config.py as example for it, you can use it to get your own version. In addition, the Dockerfile is presented, you can modify it to get your own image.

### Notes of Dockerfile
Cron job, ```30 * * * * cd /tmp && rm -r ./*```, this one is added to avoid the temp file of geckodriver taking over all the space.
