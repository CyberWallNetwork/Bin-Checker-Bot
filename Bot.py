import requests
from pyrogram import Client, filters
from configs import config
from asyncio import sleep

from pyrogram.types import (
    Message, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup
)


Bot = Client(
    ":memory:",
    api_hash=config.API_HASH,
    api_id=config.API_ID,
    bot_token=config.BOT_TOKEN,
)


@Bot.on_message(filters.command("start"))
async def start(_, m: Message):
    messy = m.from_user.mention
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Channel", url="https://t.me/szteambots"),
                InlineKeyboardButton("Support", url="https://t.me/slbotzone"),
            ],
            [
                InlineKeyboardButton(
                    "Source code", url="https://github.com/ImDenuwan/Bin-Checker-Bot"
                )
            ],
        ]
    )
    await m.reply_text(
        f"Hi! {messy} \nI can Check bins Valid or Invalid.\n\nTo see more check /help command",
        reply_markup=keyboard,
    )


@Bot.on_message(filters.command("help"))
async def help(_, m: Message):
    await m.reply_text(
        "/start - **To check bot alive**.\n/help - **To see help menu.**\n/bin [qoury] - **To check Bin is valide or Invalid.**"
    )


@Bot.on_message(filters.command("bin"))
async def bin(_, m: Message):
    if len(m.command) < 2:
        msg = await m.reply_text("Please Provide a Bin!\nEx:- `/bin 401658`")
        await sleep(15)
        await msg.delete()

    else:
        try:
            mafia = await m.reply_text("processing...")
            inputm = m.text.split(None, 1)[1]
            bincode = 6
            ask = inputm[:bincode]
            req = requests.get(f"https://lookup.binlist.net/{ask}").json()
            res = req["result"]

            if res == False:
                return await mafia.edit("❌ #INVALID_BIN ❌\n\nPlease provide a valid bin.")
            data = req["data"]
            vendor = data["scheme"]
            type = data["type"]
            prepaid = data["prepaid"]
            bankinfo = data["bank"]
            phone = bankinfo["phone"]
            bank = bankinfo["name"]
            countryinfo = data["country"]
            country = countryinfo["name"]
            emoji = countryinfo["emoji"]
            code = countryinfo["alpha2"]
            currency = countryinfo["currency"]

            mfrom = m.from_user.mention
            caption = f"""
    ->Valid - {res}\nBin - {ask}\n-> Vendor - {vendor} \n-> Type - {type} \n-> Prepaid - {prepaid} \n-> Bank - {bank} \n-> Bank Phone - {phone} \n-> Country - {country}/{code} {emoji} \n-> Currency - {currency}_
    """
            await mafia.edit(caption, disable_web_page_preview=True)
            
        except Exception as e:
            await bot.reply_text(f"**Oops Error!**\n{e}\n\n**Report This Bug to Bot Owner.**")

print("Bot IS Alive Now")

Bot.run()
