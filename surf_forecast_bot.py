import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import json
import typing_extensions as typing

from surfscarper import extract_forecast_table
from retrieveInfo import retrieveInfo\

class Response(typing.TypedDict):
    intent: str
    X: str
    Y: str
    Z: str

class TelegramBot:
    def __init__(self, bot_key, gemini_key):
        self.bot_key = bot_key
        self.gemini_key = gemini_key
        genai.configure(api_key=self.gemini_key)
        self.gemini = genai.GenerativeModel("gemini-1.5-flash")
        self.application = ApplicationBuilder().token(self.bot_key).build()
        self.setup_handlers()
        self.getSurfForecast()
        self.getIntents()
        self.getPrompt()
        self.last_question = None
        print('Bot initialized successfully!')

    def getIntents(self):
        #read intents json
        with open('intents.json') as file:
            self.intents = json.load(file)['intents']
        self.intents_list = ' \n'.join([intent for intent in self.intents])

    def getPrompt(self):
        # read prompt txt
        with open('prompt.txt') as file:
            self.prompt = file.read()

    def getSurfForecast(self):
        url = 'https://www.surf-forecast.com/breaks/Bajamar-El-Lobo/forecasts/latest/six_day'

        # Send a GET request to the website
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the forecast data
        self.forecast = extract_forecast_table(soup)
        self.days = self.forecast.columns[1:].tolist()
        self.categories = self.forecast['Metric'].tolist()

    def setup_handlers(self):
        start_handler = CommandHandler('start', self.start)
        message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_message)
        self.application.add_handler(start_handler)
        self.application.add_handler(message_handler)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, I'm the surf forecast bot!")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="At the moment, I can tell you about the surf forecast in Bajamar (El Lobo). Ask me anything!")
        # await context.bot.send_message(chat_id=update.effective_chat.id, text="Ready!")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print("Message received: " + update.message.text)
        prompt = self.prompt.format(intents_list=self.intents_list, question=update.message.text, categories=self.categories, days=self.days)
        response = self.gemini.generate_content(prompt, 
                                                generation_config=genai.GenerationConfig(response_mime_type="application/json", response_schema=Response),)
        query = json.loads(response.text)
        print("Query: " + str(query))

        if query['intent'] == 'other' and self.last_question is not None:
            prompt = "The user's last question was: " + self.last_question + ". Now they are asking a follow-up question: " + update.message.text \
                + ". Given the last question and the new question and " + prompt
            
            response = self.gemini.generate_content(prompt, 
                                                generation_config=genai.GenerationConfig(response_mime_type="application/json", response_schema=Response),)
            query = json.loads(response.text)

        if query['intent'] == 'other':
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't get that. I only know about the surf forecast.\
                                            If you asked something about the forecast, please try rephrasing your question.")
        else:
            print("Query: " + str(query))

            answer = retrieveInfo(self.forecast, query)
            print("Answer: " + str(answer))

            prompt = "It has been found that the answer to the user's question " + update.message.text + " is: " + str(answer) + ". Communicate this answer to the user."
            text = self.gemini.generate_content(prompt).text

            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        
        self.last_question = update.message.text

    def run(self):
        self.application.run_polling()

if __name__ == '__main__':
    load_dotenv()  # take environment variables from .env
    BOT_KEY = os.environ.get("SURF_FORECAST_BOT_API_KEY")
    GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

    bot = TelegramBot(BOT_KEY, GEMINI_KEY)
    bot.run()