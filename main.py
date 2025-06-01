import os
import asyncio
from datetime import datetime, time
from telethon import TelegramClient, events, functions, types

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))
UPDATE_CHANNEL_ID = int(os.getenv("UPDATE_CHANNEL_ID"))
PUBLIC_CHANNEL_USERNAME = os.getenv("PUBLIC_CHANNEL_USERNAME")

ADMINS = list(map(int, os.getenv("ADMINS", "").split()))
TIP_TIMINGS = os.getenv("TIP_TIMINGS", "10:00,23:00").split(",")

client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

tips_file = "tips.json"

import json

async def send_tip(tip_text):
    await client.send_message(PUBLIC_CHANNEL_USERNAME, tip_text)
    await client.send_message(LOG_CHANNEL_ID, f"Sent tip: {tip_text}")

async def load_tips():
    try:
        with open(tips_file, "r") as f:
            return json.load(f)
    except Exception:
        return []

async def save_tips(tips):
    with open(tips_file, "w") as f:
        json.dump(tips, f, indent=2)

@client.on(events.NewMessage(pattern="/edit_tip"))
async def edit_tip_handler(event):
    if event.sender_id not in ADMINS:
        await event.reply("Unauthorized")
        return
    args = event.message.text.split(maxsplit=1)
    if len(args) < 2:
        await event.reply("Usage: /edit_tip <new tip text>")
        return
    new_tip = args[1].strip()
    tips = await load_tips()
    if tips:
        tips[0] = new_tip
    else:
        tips.append(new_tip)
    await save_tips(tips)
    await event.reply(f"Tip updated to {new_tip}")
    await client.send_message(LOG_CHANNEL_ID, f"Tip edited by admin: {new_tip}")

async def daily_tip_scheduler():
    while True:
        now = datetime.now().time()
        tips = await load_tips()
        for tt in TIP_TIMINGS:
            hh, mm = map(int, tt.split(":"))
            target = time(hh, mm)
            if now.hour == target.hour and now.minute == target.minute:
                if tips:
                    await send_tip(tips[0])
        await asyncio.sleep(60)

@client.on(events.NewMessage(chats=UPDATE_CHANNEL_ID))
async def forward_updates(event):
    await client.forward_messages(PUBLIC_CHANNEL_USERNAME, event.message)
    await client.send_message(LOG_CHANNEL_ID, f"Forwarded message ID {event.message.id}")

async def main():
    await client.start()
    client.loop.create_task(daily_tip_scheduler())
    print("Bot started...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
