from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from htmlPdf import pdf
from py_dotenv import read_dotenv
import os
from analitycs import nuovoUtente, ricerche
import threading
from server import run

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
read_dotenv(dotenv_path)

name = None
bot = Bot(os.getenv("API_BOT"))
updater = Updater(os.getenv("API_BOT"), use_context=True)


def bot():
    global updater
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    def start(update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        update.message.reply_text(
            'Benvenuto nel bot di corsiuniversitari.info \nhttps://www.corsiuniversitari.info')
        update.message.reply_text('Quale corso stai cercando?')
        nuovoUtente()

    def cerca(update: Update, context: CallbackContext) -> None:
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
                InlineKeyboardButton(
                    "Master di primo livello", callback_data='6'),
                InlineKeyboardButton(
                    "Master di secondo livello", callback_data='7'),
            ],

            reply_markup = InlineKeyboardMarkup(keyboard)

            query.edit_message_text(
                'Hai scelto master, quali?', reply_markup=reply_markup)

        if query.data == '3':
            query.message.reply_text('Tra un attimo arriverà un pdf.')
            file = pdf(name, 1, 'Triennale')
            if file == 0:
                query.message.reply_text('Pare che questo corso non esista.')
            else:
                query.bot.send_document(
                    chat_id=chat_id, document=file, filename='report.pdf', caption=None,)
                query.message.reply_text('Pdf generato.')
            ricerche('Triennale', name)

        if query.data == '4':
            query.message.reply_text('Tra un attimo arriverà un pdf.')
            file = pdf(name, 1, 'Magistrale a Ciclo Unico')
            if file == 0:
                query.message.reply_text('Pare che questo corso non esista.')
            else:
                query.bot.send_document(
                    chat_id=chat_id, document=file, filename='report.pdf', caption=None,)
                query.message.reply_text('Pdf generato.')
            ricerche('Magistrale a Ciclo Unico', name)

        if query.data == '5':
            query.message.reply_text('Tra un attimo arriverà un pdf.')
            file = pdf(name, 1, 'Magistrale')
            if file == 0:
                query.message.reply_text('Pare che questo corso non esista.')
            else:
                query.bot.send_document(
                    chat_id=chat_id, document=file, filename='report.pdf', caption=None,)
                query.message.reply_text('Pdf generato.')
            ricerche('Magistrale', name)

        if query.data == '6':
            query.message.reply_text('Tra un attimo arriverà un pdf.')
            file = pdf(name, 2, 'Master di Primo Livello')
            if file == 0:
                query.message.reply_text('Pare che questo corso non esista.')
            else:
                query.bot.send_document(
                    chat_id=chat_id, document=file, filename='report.pdf', caption=None,)
                query.message.reply_text('Pdf generato.')
            ricerche('Master di Primo Livello', name)

        if query.data == '7':
            query.message.reply_text('Tra un attimo arriverà un pdf.')
            file = pdf(name, 2, 'Master di Secondo Livello')
            if file == 0:
                query.message.reply_text('Pare che questo corso non esista.')
            else:
                query.bot.send_document(
                    chat_id=chat_id, document=file, filename='report.pdf', caption=None,)
                query.message.reply_text('Pdf generato.')
            ricerche('Master di Secondo Livello', name)

    def risposta(update: Update, context: CallbackContext) -> None:
        global name
        name = update.message.text

        keyboard = [
            InlineKeyboardButton("Corsi di laurea", callback_data='1'),
            InlineKeyboardButton("Master", callback_data='2'),
        ],

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(
            'Cosa stai cercando?', reply_markup=reply_markup)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("cerca_corso", cerca))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, risposta))

    # Start the Bot
    updater.start_polling()


def main():
    os.chdir(os.getcwd() + '/server')
    threads = list()
    # web server
    server = threading.Thread(target=run, args=(), daemon=True)
    server.start()
    # bot
    x = threading.Thread(target=bot, args=())
    x.start()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
