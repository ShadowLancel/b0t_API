#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from distutils.util import convert_path
from dotenv import load_dotenv
import logging
from telegram.ext import CallbackContext, CallbackQueryHandler
from telegram import __version__ as TG_VER
import telegram
import requests

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler

bot = telegram.Bot(token=os.getenv('TG_BOT_TOKEN'))
url = 'https://svcs.ebay.com/services/search/FindingService/v1'
operation_name = 'findItemsByKeywords'
app_id = os.getenv('APP_ID-ebay')
PRODUCT_NAME, PROD_PER_PAGE, FINAL_ID = range(3)
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"H0i {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )
    return PRODUCT_NAME

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("BoT gIv 4r U Anketa. Yo fiL 1t sAmm wrds abAut prdUct Nnd h3s taKe f4r u l1nk abut prAdct 0n Magazine eBay.")

async def search(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /search is issued."""
    await update.message.reply_text("4 ur Se4rCh nId Fil ANKETA. FoRsT qWest10n : WhAT N4m3 Pr0dct")
    return PROD_PER_PAGE

async def product_name(update, context):
    user_data = {}
    user_data['product_name'] = update.message.text
    context.user_data.update(user_data)
    logger.info('pr_nm: %s', user_data['product_name'])
    await update.message.reply_text('SeCnd QwsTioN : hAw MatCH Pr0dct U NiD? 1 dO 100')
    return FINAL_ID

async def prod_per_page(update, context):
    user_data = context.user_data
    user_data['prod_per_page'] = update.message.text
    logger.info('PPP: %s', user_data['prod_per_page'])
    await bot.send_message(chat_id=update.effective_chat.id, text='ThX U 4r Ur InPt!')
    product_name = user_data['product_name']
    prod_per_page = user_data['prod_per_page']
    # Задаем заголовки запроса
    headers = {
    'X-EBAY-SOA-OPERATION-NAME': operation_name,
    'X-EBAY-SOA-SECURITY-APPNAME': app_id,
    'X-EBAY-SOA-RESPONSE-DATA-FORMAT': 'JSON'
              }

    # Параметры запроса
    params = {
    'keywords': product_name,
    'paginationInput': {
        'entriesPerPage': prod_per_page, # От 1 До 100 запросов
        'pageNumber': 1
                       }
             }
    # Send a request to the API with the headers and parameters
    response = requests.get(url, headers=headers, params=params)
    # Parse the response and send it back to the user via Telegram bot
    if response.status_code == 200:
        data = response.json()
        i = 0
        search_result = data.get('findItemsByKeywordsResponse')[0].get('searchResult')[0]
        for item in search_result.get('item'):
            if i >= int(prod_per_page):
                break
            message = f"HIr Ar3 thE reSlts 4 {product_name}: {item.get('title')[0]} . URL: {item.get('viewItemURL')[0]}"
            await bot.send_message(chat_id=update.effective_chat.id, text=message)
            i+=1
            logger.info('i: %s', i)
    else:
        message = f"Sry, thEr wAs An Errr wOth th3 API rEqu3st. Errr c0d: {response.status_code}"
        await bot.send_message(chat_id=update.effective_chat.id, text=message)

    return ConversationHandler.END

async def cancel(update, context):
    await bot.send_message(chat_id=update.effective_chat.id, text='C0nvrs4t1On cAncll3d. WrAiT /Start 4 BeG1n sEarCH aGa1n.')
    return ConversationHandler.END

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv('TG_BOT_TOKEN')).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PRODUCT_NAME: [CommandHandler('search', search)],
            PROD_PER_PAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, product_name)],
            FINAL_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, prod_per_page)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    # on different commands - answer in Telegram
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))
    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()   