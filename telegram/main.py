import asyncio
from aiogram import Bot, Dispatcher, Router, F
import logging
import sys
from db.database import init_user_db ,  get_user_full_profile, save_or_update_user
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from profiledir import profile
from tests import MBTI, enneagram
from tests.enneagram_types import enneagram_types

CHANNEL_USERNAME = "itsjudttest"
API_TOKEN = "8030278969:AAEavE9AgS5YPGV3UhgQT3vlT1TTKDhm4ZU"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()




main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧠 تست ها")],
        [KeyboardButton(text="💬 چت ناشناس (به زودی)"), KeyboardButton(text="🎲 سرگرمی و تست فان (به زودی)")],
        [KeyboardButton(text="🎥 فیلم و مدیا (به زودی)"),KeyboardButton(text="👤 پروفایل")],
        [KeyboardButton(text="🎖️ چالش روزانه (به زودی)"), KeyboardButton(text="📚 ویکی‌بات (به زودی)")],
        [KeyboardButton(text="📊 رتبه‌بندی (به زودی)"), KeyboardButton(text="🎁 کیف پول (به زودی)") , KeyboardButton(text="📞 پشتیبانی")]
    ],
    resize_keyboard=True,
    input_field_placeholder="یک گزینه رو انتخاب کن..."
)



dp.include_router(router)
dp.include_router(MBTI.router)
dp.include_router(profile.router)
dp.include_router(enneagram.router)


@router.message(Command(commands="start"))
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id

    # ۱. پیام خوش‌آمد (همیشه اول)
    await message.answer(
        "سلام رفیق! 👋✨\n"
        "اینجا کلی تست‌ جذاب و متفاوت منتظرتن تا بهتر خودت رو کشف کنی.\n"
        "قول می‌دم هر لحظه با این ربات حسابی کیف کنی! 😄🎉"
    )

    await message.answer(
        "دمت گرم که به این ربات سر زدی ولی متاسفانه ربات هنوز کامل نیست و تیم ما درحال ساخت این ربات هستند به همین دلیل شما قادر به استفاده از تمامی خدمات نیستید. با تشکر"
    )

    # ۲. بررسی عضویت در کانال
    member = await bot.get_chat_member(chat_id=f"@{CHANNEL_USERNAME}", user_id=user_id)
    if member.status not in ("member", "administrator", "creator"):
        await message.answer(
            "❌ برای استفاده از ربات باید اول عضو کانال بشی.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME}")],
                    [InlineKeyboardButton(text="✅ تایید عضویت", callback_data="verify_membership")]
                ]
            )
        )
        return  # خروج چون کاربر عضو نیست

    # ۳. بررسی اینکه آیا کاربر قبلاً پروفایل ساخته یا نه
    profile = get_user_full_profile(user_id)
    if profile:
        name = profile[1]  # ستون دوم جدول users = name
        await message.answer(f"سلام {name} جان! خوش برگشتی 😊", reply_markup=main_menu)
    else:
        await message.answer("📝 قبل از شروع، اسمتو بنویس تا پروفایلت ساخته شه:")
        await state.set_state(Register.name)


@router.message(Command(commands="test"))
async def test(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await message.answer("""🔹 ISTJ - بازرس دقیق‌نگر

🧠 عملگرا، منظم و قابل‌اعتماد

📌 تیپ ISTJ یکی از منطقی‌ترین و متعهدترین تیپ‌های شخصیتی در MBTI است. این افراد به شدت وظیفه‌شناس هستند و کارها را با دقت، تمرکز و پشتکار انجام می‌دهند.

📊 ویژگی‌های کلیدی:
• منطقی و تحلیل‌گر
• منظم و سازمان‌یافته
• پایبند به قوانین و سنت‌ها
• محتاط در تصمیم‌گیری
• قابل‌اعتماد و مسئولیت‌پذیر

💬 جملاتی که ممکن است از یک ISTJ بشنوید:
«من فقط وقتی کاری رو شروع می‌کنم که برنامه‌ریزی کامل براش داشته باشم.»
«تعهد برای من مهم‌تر از هیجانه.»

💼 شغل‌های مناسب برای ISTJ:
حسابدار، تحلیل‌گر داده، وکیل، افسر پلیس، مهندس، مدیر پروژه

❤️ در روابط:
ISTJها افرادی وفادار، صادق و محافظ‌کار هستند. آن‌ها در روابط عاطفی به دنبال ثبات، اعتماد و تعهد بلندمدت هستند و احساسات‌شان را به‌راحتی بروز نمی‌دهند، اما در عمل وفاداری‌شان را ثابت می‌کنند.

📚 نقاط قوت:
✓ سخت‌کوش
✓ متعهد
✓ واقع‌گرا
✓ جزئی‌نگر

⚠️ چالش‌ها:
✗ انعطاف‌ناپذیری
✗ دشواری در بروز احساسات
✗ قضاوت سریع نسبت به دیگران""")

@router.callback_query(F.data == "verify_membership")
async def verify_membership(callback: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = callback.from_user.id

    try:
        member = await bot.get_chat_member(chat_id=f"@{CHANNEL_USERNAME}", user_id=user_id)
        if member.status in ("member", "administrator", "creator"):
            # بررسی وجود پروفایل
            profile = get_user_full_profile(user_id)
            if profile:
                name = profile[1]
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
    # مپ کردن انتخاب جنسیت
    gender_map = {
        "gender_boy": "پسر",
        "gender_girl": "دختر",
        "gender_none": "ترجیح نمی‌دم بگم"
    }
    gender_value = gender_map.get(callback.data, "نامشخص")

    # دریافت داده‌های ذخیره‌شده در استیت
    data = await state.get_data()
    name = data.get("name") or callback.from_user.full_name
    age = data.get("age") or 0

    # ذخیره در دیتابیس پیشرفته کاربران
    save_or_update_user(
        user_id=callback.from_user.id,
        name=name,
        age=age,
        gender=gender_value,
        username=callback.from_user.username or "-",
        invite_link=f"https://t.me/persian_mbtiBot?start={callback.from_user.id}"  # اختیاری
    )

    # پیام تایید
    await callback.message.edit_text(f"✅ پروفایل با موفقیت ذخیره شد، {name} جان! آماده‌ای برای شروع تست؟ 😎")

    # نمایش منو
    await callback.message.answer("از منوی زیر یکی رو انتخاب کن:", reply_markup=main_menu)

    await state.clear()
    await callback.answer()


# MBTI test start

tests_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧠 تست‌های شخصیت")],
        [KeyboardButton(text="😟 تست‌های روان‌درمانی (به زودی)"), KeyboardButton(text="🧠 تست‌های هوش (به زودی)")],
        [KeyboardButton(text="👤 تست‌های رفتاری (به زودی)"), KeyboardButton(text="❤️ تست‌های روابط (به زودی)")],
        [KeyboardButton(text="🔙 بازگشت به منوی اصلی")],
    ],
    resize_keyboard=True,
    input_field_placeholder="چه نوع تستی میخوای بزنی؟..."
)

@router.message(F.text == "🧠 تست ها")
async def handle_mbti_button(message: Message):
    user_id = message.from_user.id
    profile = get_user_full_profile(user_id)

    if profile:
        name = profile[1]
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
    profile = get_user_full_profile(message.from_user.id)
    name = profile[1] if profile else "کاربر"

    await message.answer(f"""🎉 برگشتیم به منوی اصلی، {name} جان!
از منوی زیر یکی رو انتخاب کن:""", reply_markup=main_menu)





personality_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=" ( آماده ) MBTI – 🧩", callback_data="MBTI_test")],
        [InlineKeyboardButton(text=" (به زودی)Big Five – 🧠", callback_data="BigFive_test"),
        InlineKeyboardButton(text=" (درحال ساخت)Enneagram – 🔺", callback_data="enneagram_menu")],
        [InlineKeyboardButton(text=" (به زودی)HEXACO – 🔶", callback_data="HEXACO_test"),
        InlineKeyboardButton(text=" (به زودی)DISC – 🔄", callback_data="DISC_test")],
        [InlineKeyboardButton(text="🔙 بازگشت (به زودی)", callback_data="main_menu")],
    ]
)


@router.callback_query(F.data == "main_menu")
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    profile = get_user_full_profile(callback.from_user.id)
    name = profile[1] if profile else "رفیق"

    await callback.message.answer(
        f"""🎉 برگشتیم به منوی اصلی، {name} جان!
از منوی زیر یکی رو انتخاب کن:""",
        reply_markup=main_menu
    )
    await callback.answer()



@router.message(F.text == "🧠 تست‌های شخصیت")
async def personality_test(message: Message, state: FSMContext):
    profile = get_user_full_profile(message.from_user.id)
    name = profile[1] if profile else "رفیق"
    await message.answer("""🧠 به دنیای شخصیتت خوش اومدی!
اینجا می‌تونی خودتو بهتر بشناسی، تیپ شخصیتیتو کشف کنی و حتی ببینی تو موقعیت‌های مختلف چه رفتاری داری.
یکی از تست‌های زیر رو انتخاب کن و شروع کن به خودشناسی:""", reply_markup=personality_menu)







# ---------------------------------------------

intelligence_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="IQ (مثل Raven) – 🧬", callback_data="IQ_test")],
        [InlineKeyboardButton(text="حافظه کاری – 🗂️", callback_data="memory_test")],
        [InlineKeyboardButton(text="🔙 بازگشت", callback_data="main_menu")],
    ]
)


@router.message(F.text == "🧠 تست‌های هوش")
async def Intelligence_test(message: Message, state: FSMContext):
    profile = get_user_full_profile(message.from_user.id)
    name = profile[1] if profile else "رفیق"
    await message.answer("""🧠 آماده‌ای مغزتو به چالش بکشی؟
اینجا قراره قدرت تحلیل، دقت و سرعت مغزتو تست کنیم!
از تست‌های کلاسیک هوش گرفته تا معماهایی که مغزتو به جوش میارن.
یکیو انتخاب کن و ببین چند مرده حلاجی 😏""", reply_markup=intelligence_menu)



# -------------------------------------------------


mantal_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="افسردگی بک (BDI) – 🌧️", callback_data="BDI_test")],
        [InlineKeyboardButton(text="اضطراب بک (BAI) – 😰", callback_data="BAI_test"),
        InlineKeyboardButton(text="GAD-7 (اضطراب فراگیر) – 🌀", callback_data="GAD_test")],
        [InlineKeyboardButton(text="PHQ-9 (افسردگی) – 📉", callback_data="PHQ_test"),
        InlineKeyboardButton(text="OCD (وسواس) – 🔁", callback_data="OCD_test")],
        [InlineKeyboardButton(text="🔙 بازگشت", callback_data="main_menu")],
    ]
)


@router.message(F.text == "😟 تست‌های روان‌درمانی")
async def mental_test(message: Message, state: FSMContext):
    profile = get_user_full_profile(message.from_user.id)
    name = profile[1] if profile else "زفیق"
    await message.answer("""🌿 یک قدم به سمت آرامش ذهن
این تست‌ها برای این طراحی شدن که بهت کمک کنن احساساتتو بهتر بشناسی، الگوهای رفتاری‌تو درک کنی و شاید ریشه‌ی بعضی درگیری‌های ذهنی‌تو پیدا کنی.
هر تست مثل یه آینه‌ست؛ بهت کمک می‌کنه بخش‌هایی از خودتو ببینی که شاید تا حالا متوجهشون نبودی.
آماده‌ای با خودت روبه‌رو بشی؟ 🕊️""", reply_markup=mantal_menu)




# --------------------------------------------------




Relationships_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="سبک دلبستگی – 🤝", callback_data="attachment_test")],
        [InlineKeyboardButton(text="مثلث عشق استرنبرگ – ❤️‍🔥", callback_data="Love_triangle_test"),
        InlineKeyboardButton(text="زبان‌های عشق – 💌", callback_data="love_lang_test")],
        [InlineKeyboardButton(text="🔙 بازگشت", callback_data="main_menu")],
    ]
)

@router.message(F.text == "❤️ تست‌های روابط")
async def Relationships_test(message: Message, state: FSMContext):
    profile = get_user_full_profile(message.from_user.id)
    name = profile[1] if profile else "رفیق"
    await message.answer("""❤️ رابطه‌هات چقدر سالم و واقعی‌ان؟
اینجا می‌تونی بفهمی توی روابطت چطور رفتار می‌کنی، چه نیازهایی داری و چطور با دیگران ارتباط برقرار می‌کنی.
چه توی رابطه‌ای باشی، چه مجرد، این تست‌ها بهت کمک می‌کنن خودتو توی آینه‌ی دیگران ببینی.""", reply_markup=Relationships_menu)



# --------------------------------------------------



async def main():
    init_user_db()
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
