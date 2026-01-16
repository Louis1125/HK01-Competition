# SmartElderCare Telegram Bot

Lightweight webhook bot for the HK01 competition project. Use this scaffold to connect Telegram to your local `smart-elder-care` services (notifications, alerts, simple queries).

Quickstart
1. Create a GitHub repo and push this folder.
2. Add environment variable `TELEGRAM_TOKEN` (bot token from @BotFather) in your deployment service.
3. Deploy to Railway or Render and set webhook to `https://<your-url>/webhook`.

Commands (example)
- `/start` - Welcome message
- `/help` - Help text
- `/patients` - List sample patients
- `/alert <text>` - Send alert message

See `bot.py` to extend command handlers and integrate with your medication system.
