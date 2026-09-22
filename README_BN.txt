# MD AKAS TV Official Telegram Bot

এই bot-এ আছে:
- YouTube Channel button
- Subscribe button
- Latest Videos section
- Songs & Music
- Qawwali & Naat
- Telegram Channel button
- Share Bot
- About
- Contact Admin
- /start, /help, /youtube, /latest, /songs, /qawwali, /about, /contact commands

## গুরুত্বপূর্ণ
Bot token কখনো GitHub, screenshot, chat বা public post-এ দেবেন না।

## সেটআপ
1. Python 3.10+ ব্যবহার করুন।
2. `pip install -r requirements.txt`
3. Environment variable হিসেবে `BOT_TOKEN` সেট করুন।
4. `bot.py` চালান: `python bot.py`

## নিজের তথ্য বসাবেন
`bot.py`-তে:
- `TELEGRAM_CHANNEL_URL`-এ আপনার Telegram channel link দিন।
- `ADMIN_USERNAME`-এ আপনার admin username দিন।
- `YOUTUBE_RSS`-এ আপনার YouTube channel RSS feed URL দিলে Latest Videos automatic হবে।

YouTube link ইতিমধ্যে MD AKAS TV channel-এর জন্য বসানো আছে।
