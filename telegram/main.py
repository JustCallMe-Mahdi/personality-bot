import asyncio
from aiogram import Bot, Dispatcher, Router, F
import logging
import sys
from db.database import init_user_db , save_user_profile , get_user_profile, save_latest_test, save_user_result
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton ,ReplyKeyboardRemove, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from tests import MBTI
import os
from datetime import datetime
import pytz
from aiogram import types


CHANNEL_USERNAME = "itsjudttest"
API_TOKEN = "8030278969:AAEavE9AgS5YPGV3UhgQT3vlT1TTKDhm4ZU"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()




main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧠 تست ها")],
        [KeyboardButton(text="💬 چت ناشناس"), KeyboardButton(text="🎲 سرگرمی و تست فان")],
        [KeyboardButton(text="🎥 فیلم و مدیا"), KeyboardButton(text="🎁 کیف پول")],
        [KeyboardButton(text="🎖️ چالش روزانه"), KeyboardButton(text="📊 رتبه‌بندی")],
        [KeyboardButton(text="📚 ویکی‌بات"), KeyboardButton(text="📞 پشتیبانی")]
    ],
    resize_keyboard=True,
    input_field_placeholder="یک گزینه رو انتخاب کن..."
)



dp.include_router(router)
dp.include_router(MBTI.router)

@router.message(Command(commands="start"))
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id

    # همیشه اول پیام خوش‌آمد بده
    welcome_text = """
سلام رفیق! 👋✨
اینجا کلی تست‌ جذاب و متفاوت منتظرتن تا بهتر خودت رو کشف کنی.
قول می‌دم هر لحظه با این ربات حسابی کیف کنی! 😄🎉
    """
    await message.answer(welcome_text)

    try:
        # بررسی عضویت در کانال
        member = await bot.get_chat_member(chat_id=f"@{CHANNEL_USERNAME}", user_id=user_id)

        if member.status in ("member", "administrator", "creator"):
            profile = get_user_profile(user_id)

            if profile:
                name = profile[0]
                await message.answer(f"سلام {name} جان! خوش برگشتی 😊", reply_markup=main_menu)
            else:
                await message.answer("📝 قبل از شروع، اسمتو بنویس تا پروفایلت ساخته شه:")
                await state.set_state(Register.name)

        else:
            await message.answer(
                "❌ برای استفاده از ربات باید اول عضو کانال بشی.",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME}")],
                        [InlineKeyboardButton(text="✅ تایید عضویت", callback_data="verify_membership")]
                    ]
                )
            )
    except Exception as e:
        await message.answer(
            "⚠️ نتونستم بررسی کنم که عضو کانال هستی یا نه.\nولی شاید هنوز عضو نشدی!\nاول عضو شو بعدش تایید کن.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME}")],
                    [InlineKeyboardButton(text="✅ تایید عضویت", callback_data="verify_membership")]
                ]
            )
        )



@router.callback_query(F.data == "verify_membership")
async def verify_membership(callback: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = callback.from_user.id

    try:
        member = await bot.get_chat_member(chat_id=f"@{CHANNEL_USERNAME}", user_id=user_id)
        if member.status in ("member", "administrator", "creator"):
            # بررسی وجود پروفایل
            profile = get_user_profile(user_id)
            if profile:
                name = profile[0]
                await callback.message.edit_text(f"✅ {name} جان، عضویتت قبلاً تایید شده و پروفایلت هم ساخته شده! بزن بریم 😎")
                await callback.message.answer(
                    "از منوی زیر یکی رو انتخاب کن:",
                    reply_markup=main_menu
                )
                await state.clear()
            else:
                await callback.message.edit_text(
                    "📝 خیلی خب، قبل از شروع باید پروفایلتو بسازیم.\nاسمتو برام بنویس:"
                )
                await state.set_state(Register.name)

        else:
            await callback.message.answer("❌ هنوز عضو کانال نشدی. لطفاً اول عضو شو و دوباره امتحان کن.")
    except Exception:
        await callback.message.answer("⚠️ مشکلی پیش اومد موقع بررسی عضویت. دوباره تلاش کن.")
    await callback.answer()


class Register(StatesGroup):
    name = State()
    age = State()

# دکمه شروع - مرحله اول
@router.callback_query(F.data == "start_profile")
async def ask_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Register.name)
    await callback.message.edit_text("📝 اسمتو برام بنویس:")
    await callback.answer()

# دریافت اسم
@router.message(Register.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer(" 📆 سنت چنده؟ (به اعداد انگلیسی بنویس)")

# دریافت سن
@router.message(Register.age)
async def get_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)

    # ساخت دکمه‌های جنسیت
    gender_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👦 پسر", callback_data="gender_boy"),
                InlineKeyboardButton(text="👧 دختر", callback_data="gender_girl"),
            ],
            [
                InlineKeyboardButton(text="❓ ترجیح می‌دم نگم", callback_data="gender_none")
            ]
        ]
    )

    # تغییر پیام با دکمه‌ها
    await message.answer(
        "🔻 جنسیتتو انتخاب کن:",
        reply_markup=gender_keyboard
    )

# دریافت جنسیت
@router.callback_query(F.data.startswith("gender_"))
async def get_gender(callback: CallbackQuery, state: FSMContext):
    gender_map = {
        "gender_boy": "پسر",
        "gender_girl": "دختر",
        "gender_none": "ترجیح نمی‌دم بگم"
    }
    gender_value = gender_map[callback.data]

    # گرفتن دیتاها و ذخیره در دیتابیس
    data = await state.get_data()
    name = data.get("name")
    age = data.get("age")
    gender = gender_value

    # فرض: این تابع اطلاعات را ذخیره می‌کند
    save_user_profile(callback.from_user.id, name, age, gender)

    await callback.message.edit_text(
        f"✅ پروفایل با موفقیت ساخته شد، {name} جان! آماده‌ای برای شروع تست؟ 😎"
    )

    await callback.message.answer(
        "از منوی زیر یکی رو انتخاب کن:",
        reply_markup=main_menu
    )

    await state.clear()
    await callback.answer()


# MBTI test start

tests_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧠 تست‌های شخصیت")],
        [KeyboardButton(text="😟 تست‌های روان‌درمانی"), KeyboardButton(text="🧠 تست‌های هوش")],
        [KeyboardButton(text="👤 تست‌های رفتاری"), KeyboardButton(text="❤️ تست‌های روابط")],
        [KeyboardButton(text="🔙 بازگشت به منوی اصلی")],
    ],
    resize_keyboard=True,
    input_field_placeholder="چه نوع تستی میخوای بزنی؟..."
)

@router.message(F.text == "🧠 تست ها")
async def handle_mbti_button(message: Message):
    user_id = message.from_user.id
    profile = get_user_profile(user_id)

    if profile:
        name = profile[0]
        await message.answer(
            f"ما اینجا انواع تست هارو داریم {name} جان! کدوم رو انتخاب میکنی؟",
            reply_markup=tests_menu
        )
    else:
        await message.answer("❗ اول باید پروفایلتو بسازی. لطفاً /start رو بزن.")


from aiogram.types import CallbackQuery
from aiogram import F

@router.message(F.text == "🔙 بازگشت به منوی اصلی")
async def back_to_main_menu(message: Message):
    profile = get_user_profile(message.from_user.id)
    name = profile[0] if profile else "کاربر"

    await message.answer(f"""🎉 برگشتیم به منوی اصلی، {name} جان!
از منوی زیر یکی رو انتخاب کن:""", reply_markup=main_menu)





personality_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="MBTI – 🧩", callback_data="MBTI_test")],
        [InlineKeyboardButton(text="Big Five – 🧠", callback_data="BigFive_test"),
        InlineKeyboardButton(text="Enneagram – 🔺", callback_data="Enneagram_test")],
        [InlineKeyboardButton(text="HEXACO – 🔶", callback_data="HEXACO_test"),
        InlineKeyboardButton(text="DISC – 🔄", callback_data="DISC_test")],
        [InlineKeyboardButton(text="🔙 بازگشت", callback_data="main_menu")],
    ]
)


@router.callback_query(F.data == "main_menu")
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    profile = get_user_profile(callback.from_user.id)
    name = profile[0] if profile else "رفیق"

    await callback.message.answer(
        f"""🎉 برگشتیم به منوی اصلی، {name} جان!
از منوی زیر یکی رو انتخاب کن:""",
        reply_markup=main_menu
    )
    await callback.answer()



@router.message(F.text == "🧠 تست‌های شخصیت")
async def personality_test(message: Message, state: FSMContext):
    profile = get_user_profile(message.from_user.id)
    name = profile[0] if profile else "رفیق"
    await message.answer("""🧠 به دنیای شخصیتت خوش اومدی!
اینجا می‌تونی خودتو بهتر بشناسی، تیپ شخصیتیتو کشف کنی و حتی ببینی تو موقعیت‌های مختلف چه رفتاری داری.
یکی از تست‌های زیر رو انتخاب کن و شروع کن به خودشناسی:""", reply_markup=personality_menu)







async def main():
    init_user_db()
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
