import os
import html
import xml.etree.ElementTree as ET
from urllib.parse import quote
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()

YOUTUBE_URL = "https://youtube.com/@mdakastv"
YOUTUBE_RSS = "https://www.youtube.com/feeds/videos.xml?channel_id=UCXXXXXXXXXXXXXXX"
# Replace YOUTUBE_RSS above with the RSS feed URL for your channel if you want
# the "Latest Videos" button to show new uploads automatically.

TELEGRAM_CHANNEL_URL = "https://t.me/your_channel"
ADMIN_USERNAME = "your_admin_username"

BOT_USERNAME = "MD_AKAS_TV_Bot"

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("▶️ YouTube Channel", url=YOUTUBE_URL)],
        [InlineKeyboardButton("🔔 Subscribe Now", url=YOUTUBE_URL)],
        [InlineKeyboardButton("🆕 Latest Videos", callback_data="latest")],
        [InlineKeyboardButton("🎵 Songs & Music", callback_data="songs")],
        [InlineKeyboardButton("🕌 Qawwali & Naat", callback_data="qawwali")],
        [InlineKeyboardButton("📢 Join Telegram", url=TELEGRAM_CHANNEL_URL)],
        [InlineKeyboardButton("📤 Share Bot", callback_data="share")],
        [InlineKeyboardButton("ℹ️ About MD AKAS TV", callback_data="about")],
        [InlineKeyboardButton("💬 Contact Admin", callback_data="contact")],
    ])

def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Menu", callback_data="home")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🎬 <b>MD AKAS TV Official Bot</b>\n\n"
        "স্বাগতম! এখানে MD AKAS TV-এর YouTube চ্যানেল, নতুন ভিডিও, "
        "গান, কাওয়ালী ও নাতে রাসুলের আপডেট পাবেন।\n\n"
        "নিচের মেনু থেকে একটি অপশন বেছে নিন 👇"
    )
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=main_menu())

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 <b>MD AKAS TV Bot Help</b>\n\n"
        "/start — Main Menu\n"
        "/youtube — YouTube Channel\n"
        "/latest — Latest Videos\n"
        "/songs — Songs & Music\n"
        "/qawwali — Qawwali & Naat\n"
        "/about — About\n"
        "/contact — Contact Admin",
        parse_mode="HTML",
        reply_markup=main_menu(),
    )

async def youtube_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 <b>MD AKAS TV YouTube Channel</b>\n\nনতুন ভিডিও দেখতে নিচের বাটনে চাপুন।",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("▶️ Open YouTube Channel", url=YOUTUBE_URL)],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="home")],
        ]),
    )

async def latest_text():
    # This is a simple RSS reader. Replace YOUTUBE_RSS with the channel RSS feed.
    if "UCXXXXXXXX" in YOUTUBE_RSS:
        return (
            "🆕 <b>Latest Videos</b>\n\n"
            "Latest Videos automatic করতে এই ফাইলের YOUTUBE_RSS-এ আপনার "
            "YouTube channel RSS feed URL বসাতে হবে।"
        )
    try:
        r = requests.get(YOUTUBE_RSS, timeout=10)
        r.raise_for_status()
        root = ET.fromstring(r.text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entries = root.findall("atom:entry", ns)[:5]
        if not entries:
            return "🆕 এখন কোনো ভিডিও পাওয়া যায়নি।"
        lines = ["🆕 <b>Latest MD AKAS TV Videos</b>\n"]
        for e in entries:
            title = e.findtext("atom:title", default="Untitled", namespaces=ns)
            link = e.find("atom:link", ns)
            href = link.attrib.get("href", "") if link is not None else ""
            lines.append(f"• <a href=\"{html.escape(href)}\">{html.escape(title)}</a>")
        return "\n".join(lines)
    except Exception:
        return "⚠️ Latest Videos এখন লোড করা যাচ্ছে না। YouTube Channel বাটনটি ব্যবহার করুন।"

async def latest_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        await latest_text(), parse_mode="HTML", disable_web_page_preview=True,
        reply_markup=back_button()
    )

async def simple_section(update, title, body):
    await update.message.reply_text(
        f"{title}\n\n{body}", parse_mode="HTML", reply_markup=back_button()
    )

async def songs_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simple_section(
        update, "🎵 <b>Songs & Music</b>",
        "MD AKAS TV-এর গান ও মিউজিক ভিডিও দেখতে YouTube Channel-এ যান।"
    )

async def qawwali_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simple_section(
        update, "🕌 <b>Qawwali & Naat</b>",
        "কাওয়ালী, নাতে রাসুল ও ইসলামিক সাংস্কৃতিক ভিডিও দেখতে YouTube Channel-এ যান।"
    )

async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simple_section(
        update, "ℹ️ <b>About MD AKAS TV</b>",
        "MD AKAS TV — গান, কাওয়ালী, নাতে রাসুল, বিনোদন ও বিভিন্ন ভিডিও কনটেন্টের একটি YouTube Channel।"
    )

async def contact_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = ADMIN_USERNAME.lstrip("@")
    await update.message.reply_text(
        "💬 <b>Contact Admin</b>\n\n"
        f"Admin: @{html.escape(username)}\n\n"
        "নিচের বাটনে চাপ দিয়ে যোগাযোগ করুন।",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 Contact Admin", url=f"https://t.me/{username}")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="home")],
        ]),
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "home":
        await q.edit_message_text(
            "🎬 <b>MD AKAS TV Official Bot</b>\n\nনিচের মেনু থেকে একটি অপশন বেছে নিন 👇",
            parse_mode="HTML",
            reply_markup=main_menu(),
        )
    elif q.data == "latest":
        await q.edit_message_text(
            await latest_text(), parse_mode="HTML",
            disable_web_page_preview=True, reply_markup=back_button()
        )
    elif q.data == "songs":
        await q.edit_message_text(
            "🎵 <b>Songs & Music</b>\n\nMD AKAS TV-এর গান ও মিউজিক ভিডিও দেখতে YouTube Channel-এ যান।",
            parse_mode="HTML", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("▶️ Open YouTube", url=YOUTUBE_URL)],
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="home")]
            ])
        )
    elif q.data == "qawwali":
        await q.edit_message_text(
            "🕌 <b>Qawwali & Naat</b>\n\nকাওয়ালী ও নাতে রাসুলের ভিডিও দেখতে YouTube Channel-এ যান।",
            parse_mode="HTML", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("▶️ Open YouTube", url=YOUTUBE_URL)],
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="home")]
            ])
        )
    elif q.data == "about":
        await q.edit_message_text(
            "ℹ️ <b>About MD AKAS TV</b>\n\nগান, কাওয়ালী, নাতে রাসুল, বিনোদন ও বিভিন্ন ভিডিও কনটেন্ট।",
            parse_mode="HTML", reply_markup=back_button()
        )
    elif q.data == "contact":
        username = ADMIN_USERNAME.lstrip("@")
        await q.edit_message_text(
            f"💬 <b>Contact Admin</b>\n\nAdmin: @{html.escape(username)}",
            parse_mode="HTML", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💬 Contact Admin", url=f"https://t.me/{username}")],
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="home")]
            ])
        )
    elif q.data == "share":
        share_url = f"https://t.me/share/url?url={quote('https://t.me/' + BOT_USERNAME)}&text={quote('MD AKAS TV Official Bot')}"
        await q.edit_message_text(
            "📤 <b>Share MD AKAS TV Bot</b>\n\nবন্ধুদের সাথে বটটি শেয়ার করুন।",
            parse_mode="HTML", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📤 Share Bot", url=share_url)],
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="home")]
            ])
        )

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is missing.")
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("youtube", youtube_cmd))
    app.add_handler(CommandHandler("latest", latest_cmd))
    app.add_handler(CommandHandler("songs", songs_cmd))
    app.add_handler(CommandHandler("qawwali", qawwali_cmd))
    app.add_handler(CommandHandler("about", about_cmd))
    app.add_handler(CommandHandler("contact", contact_cmd))
    app.add_handler(CallbackQueryHandler(handle_callback))

    print("MD AKAS TV Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
