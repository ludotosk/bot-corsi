from telegram import *
from telegram.ext import *
from htmlPdf import pdf
from dotenv import load_dotenv
import os
load_dotenv()
from server import run
import threading

name = None
bot = Bot(os.getenv("API_BOT"))
updater = Updater(os.getenv("API_BOT"), use_context=True)

def main():
    global updater
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher


    def start(update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        update.message.reply_text(
            'Benvenuto nel bot di corsiuniversitari.info \nhttps://www.corsiuniversitari.info')
        update.message.reply_text('Quale corso stai cercando?')


    def cerca(update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        update.message.reply_text('Quale corso stai cercando?')


    def button(update: Update, context: CallbackContext) -> None:        
        query = update.callback_query
        chat_id = query.message.chat_id
        global name

        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        query.answer()

        # query.edit_message_text(text=f"Hai scelto: {query.data}")

        if query.data == '1':
            keyboard = [
                [InlineKeyboardButton("Triennali", callback_data='3')],
                [InlineKeyboardButton(
                    "Magistrali a ciclo unico", callback_data='4')],
                [InlineKeyboardButton("Magistrali", callback_data='5')],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            query.edit_message_text(
                'Hai scelto corsi di laurea, quali?', reply_markup=reply_markup)

        if query.data == '2':
            keyboard = [
                InlineKeyboardButton("Master di primo livello", callback_data='6'),
                InlineKeyboardButton(
                    "Master di secondo livello", callback_data='7'),
            ],

            reply_markup = InlineKeyboardMarkup(keyboard)

            query.edit_message_text(
                'Hai scelto master, quali?', reply_markup=reply_markup)

        if query.data == '3':
            query.message.reply_text('Tra un attimo arriverà un pdf.')
            file = pdf(name,1,'Triennale')
            query.bot.send_document(chat_id=chat_id, document = file, filename = 'report.pdf', caption = None,)
            query.message.reply_text('Pdf generato.')

        if query.data == '4':
            query.message.reply_text('Tra un attimo arriverà un pdf.')
            file = pdf(name,1,'Triennale')
            query.bot.send_document(chat_id=chat_id, document = file, filename = 'report.pdf', caption = None,)
            query.message.reply_text('Pdf generato.')

        if query.data == '5':
            query.message.reply_text('Tra un attimo arriverà un pdf.')
            file = pdf(name,1,'Triennale')
            query.bot.send_document(chat_id=chat_id, document = file, filename = 'report.pdf', caption = None,)
            query.message.reply_text('Pdf generato.')
            
        if query.data == '6':
            print('nulla')

        if query.data == '7':
            print('nulla')

        

    def risposta(update: Update, context: CallbackContext) -> None:
        global name
        name = update.message.text

        keyboard = [
            InlineKeyboardButton("Corsi di laurea", callback_data='1'),
            InlineKeyboardButton("Master", callback_data='2'),
        ],

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Cosa stai cercando?', reply_markup=reply_markup)


    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))

    dispatcher.add_handler(CommandHandler("cerca_corso", cerca))

    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, risposta))

    # Start the Bot
    updater.start_polling()  

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
  
if __name__ == "__main__":
    main()