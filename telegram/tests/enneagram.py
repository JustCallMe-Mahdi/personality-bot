from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from db.database import get_user_full_profile
from tests.enneagram_types.enneagram_types import get_enneagram_type_description

router = Router()

def enneagram_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔹ساده (18 سوال)", callback_data="enneagram_simple_start"),
        InlineKeyboardButton(text="🔸پیشرفته (45 سوال)", callback_data="enneagram_advanced")],
        [InlineKeyboardButton(text="📘 رهنما", callback_data="enneagram_guide"),
        InlineKeyboardButton(text="📚 آشنایی با تیپ ها", callback_data="enneagram_types")],
        [InlineKeyboardButton(text="🔙 بازگشت", callback_data="back_to_tests")]
    ])
    return keyboard

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


@router.callback_query(F.data == "back_to_tests")
async def back_to_tests(callback: CallbackQuery):
    user_id = callback.from_user.id
    profile = get_user_full_profile(user_id)

    if profile:
        name = profile[1]
        await callback.message.answer(
            f"ما اینجا انواع تست هارو داریم {name} جان! کدوم رو انتخاب میکنی؟",
            reply_markup=tests_menu
        )
    else:
        await callback.message.answer("❗ اول باید پروفایلتو بسازی. لطفاً /start رو بزن.")


@router.callback_query(F.data == "enneagram_menu")
async def enneagram_menu_handler(callback: CallbackQuery):
    text = (
        """<b>🧠 تست شخصیت Enneagram: لایه‌ی پنهان شخصیتت رو بشناس!</b>
این تست یکی از عمیق‌ترین تست‌های شخصیت‌شناسی دنیاست.
انیاگرام کمک می‌کنه بفهمی چرا واقعاً اون‌جوری رفتار می‌کنی که می‌کنی — نه فقط چطور!

🎯 قراره با ترس‌های پنهان، انگیزه‌های درونی، نقاط قوت و حتی مسیر رشد شخصیتت آشنا بشی.
کافیه فقط انتخاب کنی:"""
    )

    await callback.message.edit_text(
        text,
        reply_markup=enneagram_menu_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


def enneagram_guide_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔹 شروع تست ساده", callback_data="enneagram_simple_start"),
        InlineKeyboardButton(text="🔸 شروع تست پیشرفته", callback_data="enneagram_advanced")],
        [InlineKeyboardButton(text="📚 آشنایی با ۹ تیپ", callback_data="enneagram_types")],
        [InlineKeyboardButton(text="🔙 بازگشت", callback_data="enneagram_menu")]
    ])
    return keyboard


def get_all_types_keyboard() -> InlineKeyboardMarkup:
    keyboard = []
    for i in range(1, 10):
        keyboard.append([
            InlineKeyboardButton(
                text=f"{i}️⃣ تیپ {i}",
                callback_data=f"show_type_{i}"
            )
        ])
    keyboard.append([
        InlineKeyboardButton(text="🔙 بازگشت", callback_data="enneagram_menu")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@router.callback_query(F.data == "enneagram_types")
async def show_all_types(callback: CallbackQuery):
    await callback.message.edit_text(
        "📚 <b>آشنایی با ۹ تیپ شخصیتی انیاگرام</b>\n\n"
        "روی هر کدوم کلیک کن تا توضیحات اون تیپ رو ببینی:",
        parse_mode="HTML",
        reply_markup=get_all_types_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.startswith("show_type_"))
async def show_type_detail(callback: CallbackQuery):
    type_num = int(callback.data.split("_")[-1])
    desc = get_enneagram_type_description(type_num)

    await callback.message.edit_text(
        f"<b>تیپ {type_num}</b>\n\n{desc}",
        parse_mode="HTML",
        reply_markup=get_all_types_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "enneagram_guide")
async def enneagram_guide_handler(callback: CallbackQuery):
    text = ("""
<b>    📘 راهنمای تست انیاگرام</b>

تست انیاگرام یکی از معروف‌ترین ابزارهای خودشناسی در دنیاست.

برخلاف تست‌هایی مثل MBTI که بهت می‌گن "چه رفتاری داری"، انیاگرام کمک می‌کنه بفهمی:
💭 چرا این رفتار رو داری؟
😨 چه ترسی پشت رفتارهات پنهانه؟
🎯 و چه چیزی واقعاً تو رو از درون هدایت می‌کنه.

🔢 توی این تست، هر کسی به یکی از ۹ تیپ شخصیتی اصلی نزدیک‌تره:
اما همه‌ی ما ترکیبی از چند تیپ هستیم.

✨ هر تیپ:
• یک ترس بنیادین داره
• یک انگیزه‌ی درونی قوی
• یک مسیر برای رشد فردی

🔄 توی نسخه‌ی پیشرفته‌ی تست حتی:
• تیپ‌های فرعی (بال‌ها)
• مسیر رشد (integration)
• مسیر فشار (disintegration)
هم بررسی می‌شن!

اگر دنبال یک خودشناسی واقعی و عمیق هستی، این تست بهت کمک می‌کنه بفهمی واقعاً کی هستی… و چه‌طور می‌تونی بهتر بشی."""
    )

    await callback.message.edit_text(
        text,
        reply_markup=enneagram_guide_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()




simple_enneagram_questions = {
    1: {
        "text": "من همیشه تلاش می‌کنم درست و اخلاقی رفتار کنم، حتی وقتی کسی نمی‌بینه.",
        "related_type": 1  # اصلاح‌گر
    },
    2: {
        "text": "وقتی کسی کاری رو اشتباه انجام می‌ده، کنترل خودمو سخت حفظ می‌کنم.",
        "related_type": 1
    },
    3: {
        "text": "من نیاز دارم احساس کنم دیگران واقعاً به من نیاز دارن.",
        "related_type": 2  # یاری‌گر
    },
    4: {
        "text": "اگه کسی ازم تشکر نکنه، ممکنه ناراحت بشم حتی اگه کمک کردن برام مهم‌تر بوده.",
        "related_type": 2
    },
    5: {
        "text": "رسیدن به موفقیت و دیده شدن برام خیلی مهمه.",
        "related_type": 3  # موفق‌طلب
    },
    6: {
        "text": "دوست دارم دیگران منو تحسین کنن، حتی اگه نقش کوچیکی بازی کرده باشم.",
        "related_type": 3
    },
    7: {
        "text": "احساس می‌کنم با بقیه فرق دارم و دنبال معنای خاصی برای زندگی‌ام هستم.",
        "related_type": 4  # فردگرا
    },
    8: {
        "text": "گاهی احساساتی می‌شم ولی نمی‌خوام کسی متوجه بشه.",
        "related_type": 4
    },
    9: {
        "text": "من معمولاً ترجیح می‌دم تنها باشم تا اینکه در جمعی قرار بگیرم که مجبور به تعامل باشم.",
        "related_type": 5  # متفکر
    },
    10: {
        "text": "خیلی وقت‌ها قبل از شروع کاری، نیاز دارم اول همه‌چی رو خوب بفهمم.",
        "related_type": 5
    },
    11: {
        "text": "من خیلی محتاط و مراقبم که به کسی یا چیزی اعتماد نکنم بی‌دلیل.",
        "related_type": 6  # وفادار/شکاک
    },
    12: {
        "text": "وقتی تصمیم مهمی دارم، اغلب دچار شک و دودلی می‌شم.",
        "related_type": 6
    },
    13: {
        "text": "من همیشه دنبال تجربه‌های جدید و هیجان‌انگیزم.",
        "related_type": 7  # خوش‌گذران
    },
    14: {
        "text": "از اینکه زمانم صرف کارهای تکراری بشه، واقعاً ناراحت می‌شم.",
        "related_type": 7
    },
    15: {
        "text": "وقتی شرایط سخت می‌شه، خودم مسئولیت رو به‌دست می‌گیرم.",
        "related_type": 8  # رهبر/چالش‌گر
    },
    16: {
        "text": "نمی‌ذارم کسی ازم سوءاستفاده کنه، حتی اگه دعوا بشه.",
        "related_type": 8
    },
    17: {
        "text": "از درگیری بدم میاد و ترجیح می‌دم همیشه صلح برقرار باشه.",
        "related_type": 9  # صلح‌طلب
    },
    18: {
        "text": "گاهی خودم رو فراموش می‌کنم فقط برای اینکه بقیه اذیت نشن.",
        "related_type": 9
    }
}




simple_type_descriptions = {
    1: "🧠 کمال‌گرا، اصول‌محور، اخلاقی\n"
       "دنبال درست‌کاری و بهبود دنیاست. گاهی زیادی سخت‌گیر می‌شه، مخصوصاً نسبت به خودش.\n"
       "وجدان قوی داره و تلاش می‌کنه از خطا دوری کنه.",

    2: "❤️ مهربان، دلسوز، فداکار\n"
       "عمیقاً نیاز به دوست داشته شدن داره. با کمک به دیگران احساس ارزش می‌کنه.\n"
       "ولی ممکنه نیازهای خودش رو نادیده بگیره.",

    3: "🏆 بلندپرواز، هدف‌گرا، عمل‌گرا\n"
       "دنبال دیده شدن و موفقیته. برای رسیدن به موفقیت، هر تلاشی می‌کنه.\n"
       "گاهی تصویری از خودش می‌سازه که واقعی نیست.",

    4: "🎨 خلاق، احساسی، منحصر‌به‌فرد\n"
       "دنبال معنا و هویت خاص خودشه. عمیقاً احساساتی و حساسه.\n"
       "گاهی در حس متفاوت بودن غرق می‌شه.",

    5: "🧩 تحلیل‌گر، کنجکاو، مستقل\n"
       "علاقه‌مند به فهم عمیق مفاهیم و ایده‌هاست. از خالی شدن انرژی خودش می‌ترسه.\n"
       "گاهی از تعاملات اجتماعی فاصله می‌گیره.",

    6: "🛡 محتاط، وفادار، مسئولیت‌پذیر\n"
       "دنبال امنیت و اعتماد قابل اتکاست. سوالات زیاد می‌پرسه و همیشه دنبال پشتیبانیه.\n"
       "ولی ممکنه دچار شک و تردید زیاد بشه.",

    7: "🎉 پرانرژی، مشتاق، خلاق\n"
       "دنبال آزادی، تجربه‌های جدید و لذت‌بردنه. از محدود شدن و دردهای درونی فراریه.\n"
       "گاهی از تعهدهای جدی طفره می‌ره.",

    8: "🔥 قوی، مستقل، قاطع\n"
       "از کنترل شدن متنفره و خودش کنترل‌گره. دنبال عدالت و قدرت واقعی برای محافظت از خودشه.\n"
       "گاهی بیش از حد تند یا سلطه‌گر می‌شه.",

    9: "🌿 آرام، پذیرنده، هماهنگ\n"
       "از تنش و درگیری فراریه. دنبال آرامش، تعادل و صلح با همه‌ست.\n"
       "ولی ممکنه خودش رو فراموش کنه یا تصمیم‌گیری رو به تأخیر بندازه.",
}




def get_enneagram_start_options() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="✅ تست ساده (سریع)", callback_data="enneagram_simple"
        )],
        [InlineKeyboardButton(
            text="📊 تست پیشرفته (دقیق)", callback_data="enneagram_advanced"
        )],
        [InlineKeyboardButton(
            text="🔙 بازگشت", callback_data="enneagram_menu"
        )]
    ])


@router.callback_query(F.data == "enneagram_simple_start")
async def send_enneagram_intro(callback: CallbackQuery):
    await callback.message.edit_text(
        text=(
            "🧠 <b>تست ساده Enneagram</b>\n\n"
            "این یه نسخه‌ی کوتاه و سریع از تست شخصیت انیاگرامه.\n"
            "با فقط ۱۸ سوال، می‌تونه یه دید اولیه از تیپ شخصیتت بده، "
            "اما دقت این نسخه حدوداً <b>۶۰٪</b> ـه و برای تحلیل عمیق کافی نیست.\n\n"
            "اگه می‌خوای بدونی:\n"
            "🔸 شبیه کدوم تیپ‌های دیگه هم هستی؟\n"
            "🔸 نقاط رشد و چالش‌هات چیه؟\n"
            "🔸 مسیر توسعه‌ی شخصیتت چطوریه؟\n\n"
            "📊 تست پیشرفته رو بزن که با بیش از ۵۰ سوال، تحلیل دقیق‌تری بهت می‌ده.\n\n"
            "<b>می‌خوای کدوم رو شروع کنی؟</b>"
        ),
        parse_mode="HTML",
        reply_markup=get_enneagram_start_options()
    )
    await callback.answer()


class SimpleEnneagramTest(StatesGroup):
    question = State()





@router.callback_query(F.data == "enneagram_simple")
async def start_simple_enneagram(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SimpleEnneagramTest.question)
    await state.update_data(current_q=1, scores={i: 0 for i in range(1, 10)})

    await send_enneagram_question(callback.message, state)
    await callback.answer()

def get_progress_bar(current, total):
    filled = int((current / total) * 10)
    return "▓" * filled + "░" * (10 - filled) + f" {int(current/total*100)}٪"

def get_question_keyboard(q_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
         [InlineKeyboardButton(text="🟢✅ کاملاً موافق", callback_data=f"answer:{q_id}:5")],
        [InlineKeyboardButton(text="🟢 موافق", callback_data=f"answer:{q_id}:4")],
        [InlineKeyboardButton(text="🟡 بی‌نظر", callback_data=f"answer:{q_id}:3")],
         [InlineKeyboardButton(text="🟠 مخالف", callback_data=f"answer:{q_id}:2")],
        [InlineKeyboardButton(text="🔴 کاملاً مخالف", callback_data=f"answer:{q_id}:1")],
    ])


async def send_enneagram_question(message: Message, state: FSMContext):
    data = await state.get_data()
    current_q = data["current_q"]
    question_data = simple_enneagram_questions[current_q]

    progress = get_progress_bar(current_q, len(simple_enneagram_questions))

    await message.edit_text(
        f"🧠 تست شخصیت Enneagram (ساده)\n"
        f"❓ سوال {current_q} از 18\n\n"
        f"💬 <b>{question_data['text']}</b>\n\n"
        f"📊 پیشرفت: {progress}\n\n"
        f"🔘 پاسخ‌ت رو انتخاب کن:",parse_mode="HTML",
        reply_markup=get_question_keyboard(current_q)
    )

@router.callback_query(F.data.startswith("answer:"), SimpleEnneagramTest.question)
async def handle_answer(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split(":")
    q_id = int(parts[1])
    score = int(parts[2])

    question_data = simple_enneagram_questions[q_id]
    related_type = question_data["related_type"]

    data = await state.get_data()
    scores = data["scores"]
    scores[related_type] += score

    current_q = data["current_q"] + 1

    if current_q > len(simple_enneagram_questions):
        await show_enneagram_result(callback, scores)
        await state.clear()
    else:
        await state.update_data(current_q=current_q, scores=scores)
        await send_enneagram_question(callback.message, state)

    await callback.answer()


def get_simple_result_keyboard(dominant_type: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🔍 درباره تیپ من بیشتر بدونم",
            callback_data=f"show_type_{dominant_type}"
        )],
        [InlineKeyboardButton(
            text="📊 رفتن به تست پیشرفته",
            callback_data="enneagram_advanced_start"
        ),
        InlineKeyboardButton(
            text="📚 آشنایی با همه تیپ‌ها",
            callback_data="enneagram_types"
        )],
        [InlineKeyboardButton(
            text="🔙 بازگشت",
            callback_data="back_to_tests"
        )],
    ])

async def show_enneagram_result(callback: CallbackQuery, scores: dict):
    dominant_type = max(scores, key=scores.get)
    score = scores[dominant_type]

    type_names = {
        1: "تیپ 1 - اصلاح‌گر",
        2: "تیپ 2 - یاری‌گر",
        3: "تیپ 3 - موفق‌طلب",
        4: "تیپ 4 - فردگرا",
        5: "تیپ 5 - متفکر",
        6: "تیپ 6 - وفادار",
        7: "تیپ 7 - خوش‌گذران",
        8: "تیپ 8 - رهبر",
        9: "تیپ 9 - صلح‌طلب",
    }

    desc = simple_type_descriptions[dominant_type]

    await callback.message.edit_text(
        f"✅ تست تموم شد!\n\n"
        f"🎯 تیپ شخصیت شما: <b>{type_names[dominant_type]}</b>\n"
        f"🧮 مجموع امتیاز: {score}\n\n"
        f"{desc}\n\n"
        f"✨ حالا می‌تونی:\n"
        f"🔹 اطلاعات کامل‌تری از این تیپ ببینی\n"
        f"🔸 تست پیشرفته رو بزنی\n"
        f"📚 بقیه تیپ‌ها رو هم مرور کنی"
        ,
        parse_mode="HTML",
        reply_markup=get_simple_result_keyboard(dominant_type)
    )












# ------------- تست پیشرفته ___________________


advanced_enneagram_questions = {
    1: "من معمولاً در تلاش هستم همه چیز رو درست، منظم و اخلاقی انجام بدم.",
    2: "خوشحال می‌شم وقتی می‌تونم به بقیه کمک کنم، حتی اگر خودم خسته باشم.",
    3: "من تمایل دارم که خودم رو موفق و توانا نشون بدم.",
    4: "گاهی احساس می‌کنم هیچ‌کس واقعاً منو نمی‌فهمه.",
    5: "وقتم رو بیشتر صرف فکر کردن و تحلیل کردن می‌کنم تا ارتباط با آدم‌ها.",
    6: "من اغلب نگران آینده و اتفاقات غیرمنتظره هستم.",
    7: "من همیشه دنبال تجربه‌های جدید و هیجان‌انگیزم.",
    8: "من ترجیح می‌دم کنترل اوضاع دست خودم باشه.",
    9: "من معمولاً سعی می‌کنم از درگیری و تنش دوری کنم.",
    10: "من از اشتباه کردن احساس گناه می‌کنم.",
    11: "گاهی نیازهای دیگران برام مهم‌تر از نیازهای خودمه.",
    12: "من زیاد به اهدافم فکر می‌کنم و برای رسیدن بهشون تلاش می‌کنم.",
    13: "من نسبت به احساساتم حساسم و به‌سادگی تحت‌تأثیر قرار می‌گیرم.",
    14: "ترجیح می‌دم بیشتر از دور به مسائل نگاه کنم تا درگیرشون بشم.",
    15: "اگر برنامه‌ای نداشته باشم، مضطرب می‌شم.",
    16: "من معمولاً نمی‌ذارم شرایط تکراری یا خسته‌کننده بشه.",
    17: "وقتی تهدید یا ظلمی ببینم، سریع واکنش نشون می‌دم.",
    18: "من اغلب خودم رو با شرایط وفق می‌دم تا از تنش جلوگیری کنم.",
    19: "من اغلب به جزئیات اهمیت می‌دم و تلاش می‌کنم بی‌نقص باشم.",
    20: "برای من مهمه که بقیه منو به‌عنوان فردی مهربون و مفید ببینن.",
    21: "من خیلی اهل رقابت و رسیدن به سطح بالام.",
    22: "گاهی احساس می‌کنم با بقیه فرق دارم.",
    23: "من علاقه دارم مستقل باشم و زیاد از بقیه کمک نمی‌گیرم.",
    24: "وقتی به چیزی مشکوکم، دلم نمی‌خواد به راحتی اعتماد کنم.",
    25: "اگر احساس کنم حوصله‌م سر رفته، سریع دنبال کار جدیدی می‌رم.",
    26: "دوست دارم حرف نهایی رو خودم بزنم.",
    27: "من اغلب به خواسته‌های خودم بی‌توجه می‌شم تا صلح حفظ بشه.",
    28: "اگر کسی از قوانین تخطی کنه، ناراحت می‌شم.",
    29: "کمک کردن به دیگران بهم حس ارزشمندی می‌ده.",
    30: "من همیشه می‌خوام بهترین نسخه‌ی خودم باشم.",
    31: "گاهی دلم می‌خواد بدون قضاوت احساساتم رو بروز بدم.",
    32: "من به تنهایی نیاز دارم تا افکارم رو بررسی کنم.",
    33: "اگر حس کنم کسی نامطمئن یا ناپایداره، مضطرب می‌شم.",
    34: "من برای تجربه‌های جدید خیلی هیجان‌زده می‌شم.",
    35: "اگر کسی بخواد منو محدود کنه، مقابله می‌کنم.",
    36: "من برای حفظ آرامش، از مخالفت با دیگران پرهیز می‌کنم.",
    37: "من از انتقاد سازنده استقبال می‌کنم چون می‌خوام پیشرفت کنم.",
    38: "برای من مهمه که دیگران ناراحت نشن، حتی اگر خودم اذیت شم.",
    39: "من همیشه سعی می‌کنم خودم رو کارآمد نشون بدم.",
    40: "احساسات عمیق برای من اهمیت زیادی دارن.",
    41: "من سعی می‌کنم قبل از عمل، همه جوانب رو تحلیل کنم.",
    42: "من گاهی در تصمیم‌گیری مردد می‌مونم.",
    43: "من برنامه‌ریزی نکردن رو نگران‌کننده می‌دونم.",
    44: "من اگر لازم باشه، قاطع و صریح حرف می‌زنم.",
    45: "من معمولاً تلاش می‌کنم از درگیری دور بمونم، حتی اگر حرفی برای گفتن داشته باشم."
}


def calculate_enneagram_scores(user_answers: dict):
    from collections import defaultdict

    scores = defaultdict(int)
    count = defaultdict(int)

    for q_num, score in user_answers.items():
        # تیپ مربوط به این سوال
        type_num = ((q_num - 1) % 9) + 1
        scores[type_num] += score
        count[type_num] += 1

    # محاسبه درصد تطابق
    percentages = {
        t: round((scores[t] / (count[t] * 5)) * 100)
        for t in scores
    }

    dominant_type = max(percentages, key=percentages.get)

    return {
        "scores": dict(scores),
        "percentages": percentages,
        "dominant_type": dominant_type
    }




class AdvancedEnneagram(StatesGroup):
    intro = State()             # ورود به تست
    answering = State()         # در حال پاسخ دادن به سوالات
    finished = State()          # اتمام تست

def answer_scale_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=str(i), callback_data=f"adv_ans_{i}") for i in range(1, 6)]
    ])


@router.callback_query(F.data == "enneagram_advanced")
async def start_advanced(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdvancedEnneagram.answering)
    await state.update_data(current_q=1, answers={})

    q_text = advanced_enneagram_questions[1]
    await callback.message.answer(
        f"سوال ۱ از ۴۵:\n\n{q_text}",
        reply_markup=answer_scale_keyboard()
    )


@router.callback_query(F.data.startswith("adv_ans_"), AdvancedEnneagram.answering)
async def handle_advanced_answer(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_q = data["current_q"]
    answers = data["answers"]

    # استخراج پاسخ
    score = int(callback.data.split("_")[2])
    answers[current_q] = score

    # سوال بعدی
    next_q = current_q + 1
    if next_q <= 45:
        await state.update_data(current_q=next_q, answers=answers)
        q_text = advanced_enneagram_questions[next_q]

        await callback.message.edit_text(
            f"سوال {next_q} از ۴۵:\n\n{q_text}",
            reply_markup=answer_scale_keyboard()
        )
    else:
        await state.set_state(AdvancedEnneagram.finished)
        await state.update_data(answers=answers)
        await show_advanced_result(callback, answers)



def get_advanced_result(type_num: int, match_percent: int, health_level: str = "نامشخص") -> str:
    results = {
        1: {
            "title": "🎯 تیپ غالب شما: تیپ ۱ - کمال‌گرا (The Reformer)",
            "analysis": """شما فردی با وجدان، اصول‌گرا و مسئولیت‌پذیر هستید. احتمالاً به استانداردهای بالا برای خودتون و دیگران پایبندید و حس می‌کنید باید جهان رو به جای بهتری تبدیل کنید. معمولاً از بی‌عدالتی، بی‌نظمی یا بی‌اخلاقی ناراحت می‌شید و سعی می‌کنید نقش اصلاح‌گر داشته باشید.""",
            "growth": """✅ یاد بگیرید بین تلاش برای کمال و پذیرش نقص‌ها تعادل برقرار کنید  
✅ در لحظه زندگی کنید؛ نه فقط در آینده‌ی آرمانی  
✅ گاهی از دید شوخی به نقص‌ها نگاه کنید تا از فشار درونی بکاهید""",
            "wings": """🔁 تیپ‌های نزدیک شما:
- بال چپ (w9): آرام‌تر، صلح‌جوتر، درون‌گراتر  
- بال راست (w2): گرم‌تر، حمایتگر، کمک‌رسان"""
        },
        2: {
            "title": "🎯 تیپ غالب شما: تیپ ۲ - یاری‌گر (The Helper)",
            "analysis": """شما فردی دلسوز، نوع‌دوست و توجه‌گر هستید که معمولاً به نیازهای دیگران اهمیت زیادی می‌دید. به‌احتمال زیاد، کمک کردن به اطرافیان براتون ارزشمند و حتی هویت‌سازه. ولی گاهی ممکنه خواسته‌های خودتون رو نادیده بگیرید تا مورد پذیرش قرار بگیرید.""",
            "growth": """✅ یاد بگیرید خواسته‌های شخصی خودتون رو هم جدی بگیرید  
✅ مرز سالم بین کمک و فداکاری افراطی بسازید  
✅ برای کمک کردن اول مطمئن بشید واقعاً ازتون خواسته شده""",
            "wings": """🔁 تیپ‌های نزدیک شما:
- بال چپ (w1): اصول‌گراتر، ساختاری‌تر  
- بال راست (w3): جاه‌طلب‌تر، اجتماعی‌تر"""
        },
        3: {
            "title": "🎯 تیپ غالب شما: تیپ ۳ - موفقیت‌گرا (The Achiever)",
            "analysis": """شما فردی هدف‌محور، باانرژی و اهل رقابت هستید. تمایل دارید تصویر موفقی از خودتون ارائه بدید و دستاورد براتون بسیار باارزشه. احتمالاً در شرایط رقابتی رشد می‌کنید اما گاهی ممکنه خود واقعی‌تون رو فراموش کنید.""",
            "growth": """✅ سعی کنید بین دستاورد و هویت شخصی تمایز قائل بشید  
✅ از پذیرش شکست نترسید؛ گاهی شکست راه رشد واقعیه  
✅ به جای ظاهر، روی احساسات درونی هم تمرکز کنید""",
            "wings": """🔁 تیپ‌های نزدیک شما:
- بال چپ (w2): گرم‌تر و مردم‌دارتر  
- بال راست (w4): خلاق‌تر و احساسی‌تر"""
        },
        4: {
            "title": "🎯 تیپ غالب شما: تیپ ۴ - هنرمند / فردگرا (The Individualist)",
            "analysis": """شما فردی احساسی، منحصربه‌فرد و خلاق هستید. تمایل دارید عمق احساسات رو تجربه کنید و با تفاوت‌هاتون شناخته بشید. گاهی ممکنه دچار حس غم یا مقایسه با دیگران بشید و احساس خاص‌بودن یا نبودن رو تجربه کنید.""",
            "growth": """✅ خودت رو با دیگران مقایسه نکن؛ رشدت منحصر به فرده  
✅ به جای غرق شدن در احساسات، بیرون از ذهن هم حضور داشته باش  
✅ خلاقیتت رو در جهت مثبت‌سازی زندگی استفاده کن""",
            "wings": """🔁 تیپ‌های نزدیک شما:
- بال چپ (w3): پرانرژی‌تر و موفقیت‌طلب  
- بال راست (w5): تحلیل‌گرتر، درون‌گراتر"""
        },
        5: {
            "title": "🎯 تیپ غالب شما: تیپ ۵ - متفکر (The Investigator)",
            "analysis": """شما فردی تحلیل‌گر، کنجکاو و عاشق یادگیری هستید. دنیای درونی‌تون غنیه و معمولاً تمایل دارید از دور مسائل رو بررسی کنید. اما گاهی ممکنه احساس کمبود انرژی یا ترس از وابستگی به دیگران داشته باشید.""",
            "growth": """✅ به جای عقب‌نشینی، گاهی هم وارد تجربه واقعی بشو  
✅ با دیگران ارتباط واقعی و انسانی بساز، نه فقط فکری  
✅ اطلاعات رو برای عمل‌کردن استفاده کن، نه فقط ذخیره کردن""",
            "wings": """🔁 تیپ‌های نزدیک شما:
- بال چپ (w4): احساسی‌تر، هنری‌تر  
- بال راست (w6): مسئولیت‌پذیرتر، محتاط‌تر"""
        },
        6: {
            "title": "🎯 تیپ غالب شما: تیپ ۶ - وفادار (The Loyalist)",
            "analysis": """شما فردی وفادار، تحلیل‌گر و دغدغه‌مند هستید. معمولاً به امنیت و ثبات اهمیت می‌دید و به‌سختی به دیگران اعتماد کامل می‌کنید. در بحران‌ها می‌تونید منبع اعتماد و پشتیبانی باشید اما گاهی دچار اضطراب بیش از حد می‌شید.""",
            "growth": """✅ اعتماد به نفس رو با تجربه‌های تدریجی بساز  
✅ نگرانی رو تبدیل به برنامه‌ریزی مثبت کن  
✅ به غریزه‌ات هم اعتماد کن، نه فقط ترس‌ها""",
            "wings": """🔁 تیپ‌های نزدیک شما:
- بال چپ (w5): فکری‌تر، محافظه‌کارتر  
- بال راست (w7): ماجراجوتر، پرانرژی‌تر"""
        },
        7: {
            "title": "🎯 تیپ غالب شما: تیپ ۷ - خوش‌گذران / مشتاق (The Enthusiast)",
            "analysis": """شما فردی خوش‌بین، پرانرژی و ماجراجو هستید. دوست دارید تجربه‌های جدید داشته باشید و از یکنواختی فرار می‌کنید. اما گاهی ممکنه از ترس ناراحتی یا رنج، خودتون رو در سرگرمی‌ها غرق کنید.""",
            "growth": """✅ با هیجان زندگی در لحظه باش، ولی از عمق احساساتت هم فرار نکن  
✅ به جای فرار از درد، اون رو بپذیر و یاد بگیر  
✅ به مسئولیت‌هات پایبند بمون تا رشدت کامل‌تر شه""",
            "wings": """🔁 تیپ‌های نزدیک شما:
- بال چپ (w6): وفادارتر، متعهدتر  
- بال راست (w8): قوی‌تر، بااراده‌تر"""
        },
        8: {
            "title": "🎯 تیپ غالب شما: تیپ ۸ - قاطع / رهبر (The Challenger)",
            "analysis": """شما فردی قدرتمند، مستقل و اهل اقدام هستید. از آسیب‌پذیری پرهیز می‌کنید و تمایل دارید خودتون و اطرافیان‌تون رو قوی نگه دارید. در بحران‌ها رهبری خوبی دارید اما گاهی ممکنه کنترل‌گر یا تهاجمی بشید.""",
            "growth": """✅ آسیب‌پذیری رو ضعف ندون؛ قدرت واقعی در صداقته  
✅ دیگران رو شریک بدون، نه رقیب  
✅ کنترل زیاد گاهی باعث فاصله گرفتن آدم‌ها می‌شه""",
            "wings": """🔁 تیپ‌های نزدیک شما:
- بال چپ (w7): ماجراجوتر، پرتحرک‌تر  
- بال راست (w9): آرام‌تر، منعطف‌تر"""
        },
        9: {
            "title": "🎯 تیپ غالب شما: تیپ ۹ - صلح‌جو (The Peacemaker)",
            "analysis": """شما فردی آرام، پذیرا و هماهنگ‌طلب هستید. از درگیری دوری می‌کنید و به دنبال ایجاد صلح در اطراف خودتون هستید. اما گاهی ممکنه نیازهای شخصی‌تون رو نادیده بگیرید تا هماهنگی حفظ بشه.""",
            "growth": """✅ یاد بگیر نه بگی؛ نظر تو هم مهمه  
✅ از فرار از درگیری به سمت مواجهه سالم حرکت کن  
✅ انرژی‌ت رو صرف خواسته‌های واقعی‌ت کن، نه فقط سازگاری""",
            "wings": """🔁 تیپ‌های نزدیک شما:
- بال چپ (w8): قاطع‌تر، بااراده‌تر  
- بال راست (w1): اصول‌گراتر، باوجدان‌تر"""
        }
    }

    data = results.get(type_num)
    if not data:
        return "❗ تیپ شما شناسایی نشد. لطفاً تست را مجدد انجام دهید."

    return (
        f"{data['title']}\n"
        f"📊 درصد تطابق: {match_percent}٪\n\n"
        f"🧬 تحلیلی از شخصیت شما:\n\n"
        f"{data['analysis']}\n\n"
        f"🧭 مسیر رشد پیشنهادی برای شما:\n\n"
        f"{data['growth']}\n\n"
        f"{data['wings']}\n\n"
        f"📉 سطح سلامت شما در حال حاضر: {health_level}\n"
        f"(براساس پاسخ‌های شما به سؤالات مربوط به کنترل، استرس و خودانتقادی)\n\n"
        f"✨ نتیجه این تست صرفاً آغاز یک سفره، نه پایانش."
    )



async def show_advanced_result(callback: CallbackQuery, answers: dict):
    result = calculate_enneagram_scores(answers)
    dominant = result["dominant_type"]
    percent = result["percentages"][dominant]

    # فعلاً سطح سلامت ثابت (می‌تونیم بعداً هوشمند کنیم)
    health = "متوسط رو به بالا"

    final_text = get_advanced_result(
        type_num=dominant,
        match_percent=percent,
        health_level=health
    )

    await callback.message.edit_text(final_text)
