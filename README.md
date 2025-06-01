# CA Mitra Bot

## Description
Telegram bot for CA Mitra channels that sends daily tips, forwards updates from private channels to public, and allows admin to edit tips.

## Setup Instructions

1. Clone the repo
2. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Rename `.env.example` to `.env` and fill your details.
5. Run the bot:
```bash
python main.py
```

## Environment Variables
- `BOT_TOKEN` - Telegram bot token from BotFather
- `API_ID`, `API_HASH` - Telegram API credentials from my.telegram.org
- `LOG_CHANNEL_ID` - Channel ID for logs
- `UPDATE_CHANNEL_ID` - Channel ID to forward updates from
- `PUBLIC_CHANNEL_USERNAME` - Public channel username to send tips and forwards
- `ADMINS` - Comma separated user IDs allowed to edit tips
- `TIP_TIMINGS` - Comma separated times in HH:MM format to send tips daily

## Deploying on Render
- Use `render.yaml` for one-click deploy or create Python service manually.
- Set environment variables in Render dashboard.

