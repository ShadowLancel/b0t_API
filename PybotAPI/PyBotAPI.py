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
from email.message import Message
import requests
import json
import logging
from telegram.ext import CallbackContext, CallbackQueryHandler
from telegram import __version__ as TG_VER

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
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

API_TOKEN = '1678302902646058-3164985130563654200-sas3-1045-8f5-sas-l7-balancer-8080-BAL-7874'
NAME, ID_REGION = range(2)

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

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("BoT gIv 4r U Anketa. Yo fiL 1t sAmm wrds abAut prdUct Nnd h3s taKe f4r u l1nk abut prAdct 0n Russian Tovarisheskiy Magazine YandexMarket.")

async def search_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /search is issued."""
    await update.message.reply_text("4 ur Se4rCh nId Fil ANKETA. FoRsT qWest10n : WhAT N4m3 Pr0dct")
    context.user_data[NAME] = update.message.text
    logger.info('user_data: %s', context.user_data)
    return NAME

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

async def scnd_vopros(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("ScOnD qWest10n : WhAT ReGion ID?")
    context.user_data[ID_REGION] = update.message.text
    logger.info('user_data: %s', context.user_data)
    return ID_REGION


async def scnd_otvet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("OKKK")

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.

    application = Application.builder().token("6263719514:AAGj3bu4SRreXZgEnjal3SgzkO1BJsjRqkE").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("search", search_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, scnd_vopros))
    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()