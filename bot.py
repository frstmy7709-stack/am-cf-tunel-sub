import time
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# اطلاعات ربات و توکنی که فرستادی
API_ID = 2040  # مقدار پیش‌فرض تلگرام برای اپلیکیشن‌ها
API_HASH = "b18441a1ff607e10a989891a5462e627"  # مقدار پیش‌فرض تلگرام
BOT_TOKEN = "9002607226:AAEJoxSUdmoKo89J6Fb0tgJp9vTunrl3hQk"

# آیدی گروه یا کانالی که کاربر باید حتماً در آن عضو باشد (آیدی خودت را اینجا بنویس)
REQUIRED_CHANNEL = "@your_group"

app = Client("my_film_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    user_id = message.from_user.id
    
    try:
        # بررسی عضویت کاربر در گروه یا کانال
        member = await client.get_chat_member(REQUIRED_CHANNEL, user_id)
        if member.status in ["left", "kicked"]:
            raise Exception("User not member")
        
        # اگر کاربر عضو گروه بود:
        sent_msg = await message.reply_text("سلام! فیلم درخواستی شما ارسال شد 🎬 (این پیام/ویدیو پس از ۳۰ ثانیه خودبه‌خود پاک می‌شود)")
        
        # بخش ارسال ویدیو (می‌توانی آیدی ویدیو را اینجا قرار دهی)
        # video_msg = await client.send_video(message.chat.id, "FILE_ID_VIDEO")
        
        # --- بخش حذف خودکار بعد از ۳۰ ثانیه ---
        await asyncio.sleep(30)
        
        # پاک کردن پیام یا ویدیو
        # await video_msg.delete()
        await sent_msg.delete()
        
    except Exception:
        # اگر کاربر عضو نبود، دکمه‌های شیشه‌ای جوین اجباری را نمایش بده
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("عضویت در گروه 📢", url=f"https://t.me/{REQUIRED_CHANNEL.replace('@', '')}")],
            [InlineKeyboardButton("عضو شدم ✅ بررسی کن", callback_data="check_join")]
        ])
        await message.reply_text(
            "سلام! برای دریافت فیلم‌ها و استفاده از ربات، ابتدا باید در گروه ما عضو شوید:",
            reply_markup=buttons
        )

app.run()
