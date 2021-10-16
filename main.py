# Made with python3
# (C) @FayasNoushad
# Copyright permission under MIT License
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/Pixeldrain-Bot/blob/main/LICENSE

import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
import pixeldrain


Bot = Client(
    "Pixeldrain-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)


START_TEXT = """**Hello {} 😌
I am small media or file to telegra.ph link uploader bot.**

>> `I can convert under 5MB photo or video to telegraph link.`

Made by @FayasNoushad"""

HELP_TEXT = """**Hey, Follow these steps:**

➠ Just give me a media under 5MB
➠ Then I will download it
➠ I will then upload it to the telegra.ph link

**Available Commands**

/start - Checking Bot Online
/help - For more help
/about - For more about me
/status - For bot updates

Made by @FayasNoushad"""

ABOUT_TEXT = """--**About Me**-- 😎

🤖 **Name :** [Telegraph Uploader](https://telegram.me/{})

👨‍💻 **Developer :** [Fayas](https://github.com/FayasNoushad)

📢 **Channel :** [Fayas Noushad](https://telegram.me/FayasNoushad)

👥 **Group :** [Developer Team](https://telegram.me/TheDeveloperTeam)

🌐 **Source :** [👉 Click here](https://github.com/FayasNoushad/Telegraph-Uploader-Bot-V2)

📝 **Language :** [Python3](https://python.org)

🧰 **Framework :** [Pyrogram](https://pyrogram.org)

📡 **Server :** [Heroku](https://heroku.com)"""

FORCE_SUBSCRIBE_TEXT = "<code>Sorry Dear You Must Join My Updates Channel for using me 😌😉....</code>"

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⚙ Help', callback_data='help'),
        InlineKeyboardButton('About 🔰', callback_data='about'),
        InlineKeyboardButton('Close ✖️', callback_data='close')
        ]]
    )

HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🏘 Home', callback_data='home'),
        InlineKeyboardButton('About 🔰', callback_data='about'),
        InlineKeyboardButton('Close ✖️', callback_data='close')
        ]]
    )

ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🏘 Home', callback_data='home'),
        InlineKeyboardButton('Help ⚙', callback_data='help'),
        InlineKeyboardButton('Close ✖️', callback_data='close')
        ]]
    )


Bot.on_callback_query()
async def cb_handler(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT.format((await bot.get_me()).username),
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.message.delete()


@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
	reply_markup=START_BUTTONS
    )


@Bot.on_message(filters.private & filters.command(["help"]))
async def help(bot, update):
    await update.reply_text(
        text=HELP_TEXT,
      	disable_web_page_preview=True,
	reply_markup=HELP_BUTTONS
    )


@Bot.on_message(filters.private & filters.command(["about"]))
async def about(bot, update):
    await update.reply_text(
        text=ABOUT_TEXT.format((await bot.get_me()).username),
        disable_web_page_preview=True,
	reply_markup=ABOUT_BUTTONS
    )


@Bot.on_message(filters.private & filters.media)
async def media_filter(bot, update):
    message = await update.reply_text(
        text="`Processing...`",
        quote=True,
        disable_web_page_preview=True
    )
    try:
        await message.edit_text(
            text="`Downloading...`",
            disable_web_page_preview=True
        )
        media = await update.download()
        await message.edit_text(
            text="`Uploading...`",
            disable_web_page_preview=True
        )
        response = pixeldrain.upload_file(media)
        status_code = response.status_code
        data = response.json()
        try:
            os.remove(media)
        except:
            pass
        await message.edit_text(
            text="`Uploaded Successfully!`",
            disable_web_page_preview=True
        )
        if data["success"] is False:
            await message.edit_text(
                text=f"**Error {status_code}:-** `I can't fetch information of your file.`",
                disable_web_page_preview=True
            )
            return
    except Exception as error:
        await message.edit_text(
            text=f"Error :- <code>{error}</code>",
            disable_web_page_preview=True
        )
        return
    text = f"**File Name:** `{data['name']}`" + "\n"
    text += f"**Download Page:** `https://pixeldrain.com/u/{data['id']}`" + "\n"
    text += f"**Direct Download Link:** `https://pixeldrain.com/api/file/{data['id']}`" + "\n"
    text += f"**Upload Date:** `{data['date_upload']}`" + "\n"
    text += f"**Last View Date:** `{data['date_last_view']}`" + "\n"
    text += f"**Size:** `{data['size']}`" + "\n"
    text += f"**Total Views:** `{data['views']}`" + "\n"
    text += f"**Bandwidth Used:** `{data['bandwidth_used']}`" + "\n"
    text += f"**Mime Type:** `{data['mime_type']}`"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Open Link",
                    url=f"https://pixeldrain.com/api/file/{data['id']}"
                ),
                InlineKeyboardButton(
                    text="Share Link",
                    url=f"https://telegram.me/share/url?url=https://pixeldrain.com/api/file/{data['id']}"
                )
            ],
            [
                InlineKeyboardButton(text="Join Updates Channel", url="https://telegram.me/M2Botz")
            ]
        ]
    )
    await message.edit_text(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


Bot.run()
