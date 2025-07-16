from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from db.database import get_user_full_profile
from utils.profile_utils import format_progress_bar
from persiantools.jdatetime import JalaliDate
import json

router = Router()

@router.message(F.text == "👤 پروفایل")
async def profile_handler(message: Message):
    user_id = message.from_user.id
    profile = get_user_full_profile(user_id)

    if not profile:
        await message.answer("❌ پروفایلی برای شما ثبت نشده. ابتدا /start را بزنید.")
        return

    # استخراج بر اساس ترتیب دقیق جدول users
    (
        user_id, name, age, gender, username,
        birth_date, join_date, level, xp, coins,
        rank, badges_json, tests_taken_json,
        displayed_test_id, invite_link
    ) = profile

    # نوار XP
    xp_percent = int((xp / 100) * 100) if xp else 0
    xp_bar = format_progress_bar(xp_percent)

    # تاریخ عضویت
    try:
        join_date_fa = JalaliDate.fromisoformat(join_date.split()[0]).strftime("%Y/%m/%d")
    except:
        join_date_fa = "⛔ نامعتبر"

    # نشان‌ها
    badges = " | ".join(json.loads(badges_json)) if badges_json else "⛔ ندارد"

    # تست نمایشی (موقت یا از db)
    displayed_test = "❌ ثبت نشده"
    if displayed_test_id:
        displayed_test = "IQ – نمره ۱۳۰"  # نمونه نمایشی
    link = f"https://t.me/persian_mbtiBot?start={user_id}"

    # متن نهایی
    text = (f"""
👤 <b>پروفایل شما:</b>


👤 نام: {name} | سن: {age} | {gender or "نامشخص"}  

🏅 سطح: {level} (کاوشگر ذهن) | XP: %{xp_percent}
 
🧠 تست نمایشی: {displayed_test}  

💰 کوین: {coins} | 🏆 رتبه: {rank or "❌"} 

📅 عضویت: {join_date_fa}  

🔗 دعوت: <a href="{invite_link or link}">کلیک کن</a>
""".strip())

    # دکمه‌های شیشه‌ای
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✏️ ویرایش پروفایل", callback_data="edit_profile")],
            [InlineKeyboardButton(text="📈 پیشرفت من", callback_data="my_progress"),
             InlineKeyboardButton(text="🧾 سوابق تست‌ها", callback_data="test_history")],
            [InlineKeyboardButton(text="🎖 نشان‌های من", callback_data="my_badges"),
             InlineKeyboardButton(text="🎯 چالش امروز", callback_data="daily_challenge")],
            [InlineKeyboardButton(text="🗺 مسیر رشد من", callback_data="growth_path")],
            [
                InlineKeyboardButton(text="👥 دعوت دوستان", callback_data="invite_friends"),
                InlineKeyboardButton(text="🫂 مقایسه با دوستان", callback_data="compare_friends"),
                InlineKeyboardButton(text="📤 اشتراک‌گذاری پروفایل", callback_data="share_profile")
            ],
        ]
    )

    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
