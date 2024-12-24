import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
cd ~# переходим в директорию пользователя
mkdir mybot # Создаем папку mybot
cd mybot # Переходим в папку mybot
pip install virtualenv
# Но скорее всего, если вы на Linux, вы увидете сообщение о том, что вам не хватает прав для вызова подобной команды
sudo pip install virtualenv # Вот так уже лучше
virtualenv --version
virtualenv ./.pyenv
source ./.pyenv/bin/activate
{
  "ok": true,
  "result": [
    {
      "update_id": 403492974,
      "message": {
        "message_id": 3,
        "from": {
          "id": 197562409,
          "is_bot": false,
          "first_name": "*****",
          "last_name": "****",
          "username": "****",
          "language_code": "en"
        },
        "chat": {
          "id": 197562409,
          "first_name": "*****",
          "last_name": "*******",
          "username": "*******",
          "type": "private"
        },
        "date": 1580395346,
        "text": "hello"
      }
    }
  ]
}
printenv VIRTUAL_ENV # убеждаемся, что мы все еще в виртуальном окружении
pip install python-telegram-bot # Устанавливаем пакет
import os
import logging
from dotenv import load_dotenv
from telegram import Bot

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("echo-bot")

max_id = 0


def main():
    global max_id
    load_dotenv()
    token = os.environ.get("ACCESS_TOKEN")
    bot = Bot(token)
    while True:
        logger.debug("start request")
        # Мы хотим получать только новые апдейты, поэтому мы завели переменную max_id
        # и вызываем метод getUpdates с параметром offset + timeout
        updates = bot.getUpdates(offset=max_id + 1, timeout=60)
        # В этой переменной мы сохраним максимальный id из полученных сейчас updates
        max_id_in_updates = 0
        for upd in updates:
            logger.debug(f"new update with id: {upd.update_id}")
            # Может быть так, что запустив бота мы получим апдейты
            # которые произошли во время его "спячки", мы их просто отфильтруем следующим условием
            # потому как max_id будет изменен только после обработки первых апдейтов
            if max_id != 0:
                bot.sendMessage(
                    upd.message.chat_id,
                    upd.message.text,
                    reply_to_message_id=upd.message.message_id,
                )
            max_id_in_updates = (
                upd.update_id
                if upd.update_id > max_id_in_updates
                else max_id_in_updates
            )
        if max_id_in_updates and max_id != max_id_in_updates:
            max_id = max_id_in_updates
            logger.debug(f"max id is changed to {max_id_in_updates}")


if __name__ == "__main__":
    main()
    import os
    import logging
    from dotenv import load_dotenv
    from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("echo-bot")


    def echo(update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=update.message.text,
            reply_to_message_id=update.message.message_id,
        )


    def start(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hello!")


    def main():
        load_dotenv()
        token = os.environ.get("ACCESS_TOKEN")
        # Создаем экземпляр класса Updater
        updater = Updater(token, use_context=True)
        dispatcher = updater.dispatcher
        # Создаем 2 хендлера
        echo_handler = MessageHandler(Filters.text, echo)
        dispatcher.add_handler(echo_handler)
        start_handler = CommandHandler("start", start)
        dispatcher.add_handler(start_handler)
        # Начинаем запрашивать обновления от Telegram Bot API
        updater.start_polling()


    if __name__ == "__main__":
        main()
        board = list(range(1, 10))


        def draw_board(board):
            print("-" * 13)
            for i in range(3):
                print("|", board[0 + i * 3], "|", board[1 + i * 3], "|", board[2 + i * 3], "|")
                print("-" * 13)


        def take_input(player_token):
            valid = False
            while not valid:
                player_answer = input( + player_token + "? ")
                try:
                    player_answer = int(player_answer)
                except ValueError:
                    continue
                if 1 <= player_answer <= 9:
                    if str(board[player_answer - 1]) not in "XO":
                        board[player_answer - 1] = player_token
                        valid = True


        def check_win(board):
            win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
            for each in win_coord:
                if board[each[0]] == board[each[1]] == board[each[2]]:
                    return board[each[0]]
            return False


        def main(board):
            counter = 0
            win = False
            while not win:
                draw_board(board)
                if counter % 2 == 0:
                    take_input("X")
                else:
                    take_input("O")
                counter += 1

                tmp = check_win(board)
                if tmp:
                    print(tmp,)
                    win = True
                    break
                if counter == 9:
                    print(tmp)
                    break
            draw_board(board)


        main(board)
#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ["Age", "Favourite colour"],
    ["Number of siblings", "Something else..."],
    ["Done"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data: dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    await update.message.reply_text(
        "Hi! My name is Doctor Botter. I will hold a more complex conversation with you. "
        "Why don't you tell me something about yourself?",
        reply_markup=markup,
    )

    return CHOOSING


async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(f"Your {text.lower()}? Yes, I would love to hear about that!")

    return TYPING_REPLY


async def custom_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    await update.message.reply_text(
        'Alright, please send me the category first, for example "Most impressive skill"'
    )

    return TYPING_CHOICE


async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]

    await update.message.reply_text(
        "Neat! Just so you know, this is what you already told me:"
        f"{facts_to_str(user_data)}You can tell me more, or change your opinion"
        " on something.",
        reply_markup=markup,
    )

    return CHOOSING


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    await update.message.reply_text(
        f"I learned these facts about you: {facts_to_str(user_data)}Until next time!",
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("TOKEN").build()

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex("^(Age|Favourite colour|Number of siblings)$"), regular_choice
                ),
                MessageHandler(filters.Regex("^Something else...$"), custom_choice),
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
    # !/usr/bin/env python
    # pylint: disable=unused-argument
    # This program is dedicated to the public domain under the CC0 license.

    """
    Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
     https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example.
    """
    import logging

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
    from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

    # Enable logging
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    # set higher logging level for httpx to avoid all GET and POST requests being logged
    logging.getLogger("httpx").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)


    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Sends a message with three inline buttons attached."""
        keyboard = [
            [
                InlineKeyboardButton("Option 1", callback_data="1"),
                InlineKeyboardButton("Option 2", callback_data="2"),
            ],
            [InlineKeyboardButton("Option 3", callback_data="3")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Please choose:", reply_markup=reply_markup)


    async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Parses the CallbackQuery and updates the message text."""
        query = update.callback_query

        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        await query.answer()

        await query.edit_message_text(text=f"Selected option: {query.data}")


    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Displays info on how to use the bot."""
        await update.message.reply_text("Use /start to test this bot.")


    def main() -> None:
        """Run the bot."""
        # Create the Application and pass it your bot's token.
        application = Application.builder().token("TOKEN").build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button))
        application.add_handler(CommandHandler("help", help_command))

        # Run the bot until the user presses Ctrl-C
        application.run_polling(allowed_updates=Update.ALL_TYPES)


    if __name__ == "__main__":
        main()
        # !/usr/bin/env python
        # pylint: disable=unused-argument
        # This program is dedicated to the public domain under the CC0 license.

        """
        Simple Bot to print/download all incoming passport data

        See https://telegram.org/blog/passport for info about what telegram passport is.

        See https://github.com/python-telegram-bot/python-telegram-bot/wiki/Telegram-Passport
         for how to use Telegram Passport properly with python-telegram-bot.

        Note:
        To use Telegram Passport, you must install PTB via
        `pip install "python-telegram-bot[passport]"`
        """
        import logging
        from pathlib import Path

        from telegram import Update
        from telegram.ext import Application, ContextTypes, MessageHandler, filters

        # Enable logging

        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
        )

        # set higher logging level for httpx to avoid all GET and POST requests being logged
        logging.getLogger("httpx").setLevel(logging.WARNING)

        logger = logging.getLogger(__name__)


        async def msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            """Downloads and prints the received passport data."""
            # Retrieve passport data
            passport_data = update.message.passport_data
            # If our nonce doesn't match what we think, this Update did not originate from us
            # Ideally you would randomize the nonce on the server
            if passport_data.decrypted_credentials.nonce != "thisisatest":
                return

            # Print the decrypted credential data
            # For all elements
            # Print their decrypted data
            # Files will be downloaded to current directory
            for data in passport_data.decrypted_data:  # This is where the data gets decrypted
                if data.type == "phone_number":
                    logger.info("Phone: %s", data.phone_number)
                elif data.type == "email":
                    logger.info("Email: %s", data.email)
                if data.type in (
                        "personal_details",
                        "passport",
                        "driver_license",
                        "identity_card",
                        "internal_passport",
                        "address",
                ):
                    logger.info(data.type, data.data)
                if data.type in (
                        "utility_bill",
                        "bank_statement",
                        "rental_agreement",
                        "passport_registration",
                        "temporary_registration",
                ):
                    logger.info(data.type, len(data.files), "files")
                    for file in data.files:
                        actual_file = await file.get_file()
                        logger.info(actual_file)
                        await actual_file.download_to_drive()
                if (
                        data.type in ("passport", "driver_license", "identity_card", "internal_passport")
                        and data.front_side
                ):
                    front_file = await data.front_side.get_file()
                    logger.info(data.type, front_file)
                    await front_file.download_to_drive()
                if data.type in ("driver_license" and "identity_card") and data.reverse_side:
                    reverse_file = await data.reverse_side.get_file()
                    logger.info(data.type, reverse_file)
                    await reverse_file.download_to_drive()
                if (
                        data.type in ("passport", "driver_license", "identity_card", "internal_passport")
                        and data.selfie
                ):
                    selfie_file = await data.selfie.get_file()
                    logger.info(data.type, selfie_file)
                    await selfie_file.download_to_drive()
                if data.translation and data.type in (
                        "passport",
                        "driver_license",
                        "identity_card",
                        "internal_passport",
                        "utility_bill",
                        "bank_statement",
                        "rental_agreement",
                        "passport_registration",
                        "temporary_registration",
                ):
                    logger.info(data.type, len(data.translation), "translation")
                    for file in data.translation:
                        actual_file = await file.get_file()
                        logger.info(actual_file)
                        await actual_file.download_to_drive()


        def main() -> None:
            """Start the bot."""
            # Create the Application and pass it your token and private key
            private_key = Path("private.key")
            application = (
                Application.builder().token("TOKEN").private_key(private_key.read_bytes()).build()
            )

            # On messages that include passport data call msg
            application.add_handler(MessageHandler(filters.PASSPORT_DATA, msg))

            # Run the bot until the user presses Ctrl-C
            application.run_polling(allowed_updates=Update.ALL_TYPES)


        if __name__ == "__main__":
            main()