# Telegram Bot of [my website](https://www.corsiuniversitari.info/)
## What does this bot?
This bot creates pdf using the API provided by one JSON [server](https://github.com/ludotosk/json-corsi-fastify) that I'm hosting on Heroku. When you start the bot it asks you what course you are looking for, then it asks whether you are searching for a master's or for a degree and then it print the result.
## Installation (Linux)
```bash
pip install python-telegram-bot --upgrade && pip install pdfkit && sudo apt-get install wkhtmltopdf && pip install dotenv && pip install py-dotenv
```
After the installation, you have to add a .env file where you have to put API_BOT with API from the father bot.