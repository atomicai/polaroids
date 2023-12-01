import logging
import os
import pathlib
from html import escape

import dotenv
from polaroids.api.extas import generate_answer
from flask import Flask

# also we want to send cool inline buttons below, so we need to import:
from pytgbot.api_types.sendable.reply_markup import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from teleflask import Teleflask
from loguru import logger

# because we wanna send HTML formatted messages below, we need:
from teleflask.messages import HTMLMessage, TextMessage

from polaroids.telegram.telestate import TeleState, machine
from polaroids.telegram.telestate.contrib.simple import SimpleDictDriver

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)

dotenv.load_dotenv()

app = Flask(__name__)

bot = Teleflask(api_key=os.environ.get("TELEGRAM_API_KEY"), app=app)

memo = SimpleDictDriver()

machine = machine.TeleStateMachine(__name__, database_driver=memo, teleflask_or_tblueprint=bot)

machine.ASKED_QUERY = TeleState("ASKED_QUERY", machine)
machine.CONFIRM_DATA = TeleState("CONFIRM_DATA", machine)


@machine.ALL.on_command("start")
def start(update, text):
    machine.set("ASKED_QUERY")
    return TextMessage(
        text=(
            "<b>Привет! </b>Задавай вопросы, а я попробую на них ответить максимально интересно и не занудно :=) "
            "<u>Поехали!</u>"
        ),
        parse_mode="html",
    )


@machine.ASKED_QUERY.on_message("text")
def some_function(update, msg):
    query = msg.text.strip()
    print(f"Query ### {query}\n")
    response = "Some dummy response"
    machine.set("CONFIRM_DATA", data={"query": query, "response": response})
    return HTMLMessage(
        f"<u>Вопрос:</u> {escape(query)}\n---\n<u>Ответ:</u> {response}",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("👌", callback_data="confirm_true"),
                ],
                [
                    InlineKeyboardButton("🤦", callback_data="confirm_false"),
                ],
            ]
        ),
    )


@machine.CONFIRM_DATA.on_update("callback_query")
def btn_confirm(update):
    logger.log(f"Got request on CONFIRM DATA state")
    logger.log(f"See {update}")
    query = machine.CURRENT.data["query"]
    response = machine.CURRENT.data["response"]
    print(update)
    if update.callback_query.data != "confirm_true":
        return TextMessage("Жаль😟", parse_mode="text")
    # end if
    machine.ASKED_QUERY.activate()  # we are done
    return HTMLMessage("Спасибо, мне приятно!")
