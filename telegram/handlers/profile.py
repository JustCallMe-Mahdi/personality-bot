from aiogram import Router, types, F
from aiogram.types import Message
from db.database import save_user_name

router = Router()

# دیکشنری موقت برای دنبال کردن مرحله پروفایل
user_states = {}

@router.callback_query(F.data == "start_test")
async def ask_name(callback: types.CallbackQuery):
    await callback.message.answer(
        "📝 قبل از اینکه تست MBTI رو شروع کنیم، لازمه یه پروفایل کوچیک ازت بسازیم.\n\n"
        "این کار فقط چند لحظه طول می‌کشه و کمک می‌کنه:\n"
        "✅ نتایج تستت دقیق‌تر تحلیل بشن\n"
        "✅ بتونیم بعداً مسیر پیشرفتتو بهتر دنبال کنیم\n"
        "✅ تجربه‌ی شخصی‌سازی‌شده‌تری بهت بدیم\n\n"
        "نترس! اطلاعاتت پیش ما امنه و فقط برای تحلیل شخصیت استفاده می‌شه.\n\n"
        "اول از همه، بگو چی صدات کنیم؟ 😄"
    )
    user_states[callback.from_user.id] = "awaiting_name"
    await callback.answer()

@router.message()
async def handle_name(message: Message):
    user_id = message.from_user.id

    if user_states.get(user_id) == "awaiting_name":
        name = message.text.strip()
        save_user_name(user_id, name)
        user_states[user_id] = "done"
        await message.answer(f"✅ ممنون {name}! پروفایل شما ذخیره شد. بریم سراغ تست MBTI؟ 🧠")
