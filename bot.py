import logging
import requests
from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart
import sqlite3
import asyncio
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

db = 'markaz.db'
BOT_TOKEN = "7193192692:AAHR7UXgo6zkstuKsZLhi6WlRZ3Mh1Wlr2U"




class PupilStates(StatesGroup):
    first_name_state = State()
    last_name_state = State()
    age_state = State()
    image_state = State()
    address_state = State()
    phone_state = State()
    day_state = State()
    time_state = State()
    finish_state = State()

class AdverState(StatesGroup):
    adver_state = State()
    adver_desc = State()
    adver_img = State()

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
    

    def add_user(self, name, lname, age, adres, phone, image, owner_id, day, times):
        self.cursor.execute(
            "INSERT INTO pupils (phone, f_name, l_name, image, age, adress, owner, day, times) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", (phone, name, lname, image, age, adres, owner_id, day, times)
        )
        self.conn.commit()

    def get_users(self):
        self.cursor.execute(
            "SELECT f_name, l_name, age, adress, phone, image, day, times, owner FROM pupils ORDER BY id DESC;"
        )        
        result = self.cursor.fetchall()
        return result
    
    def add_adver(self, name, desc, image):
        self.cursor.execute(
            "INSERT INTO advertisiments (adver_name, adver_description, adver_img) VALUES (?, ?, ?);", (name, desc, image)
        )
        self.conn.commit()

    def get_adver(self):
        self.cursor.execute(
            "SELECT adver_name, adver_description, adver_img FROM advertisiments;"
        )
        result = self.cursor.fetchall()
        return result
    def del_from(self, db_name):
        self.cursor.execute(
            f"DELETE FROM {db_name};"
        )
        self.conn.commit()
        
command_router = Router()
pupil_router = Router()
db = Database()

register_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/Register")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
confirm = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ha", callback_data="Yes"),
            InlineKeyboardButton(text="Yo'q", callback_data="No")
        ]
    ]
)
admin_commands = [
    BotCommand(command="start", description="Qayta ishga tushirish"),
    BotCommand(command="pupils", description="Kursga yozilganlar"),
    BotCommand(command='advertisiment', description="E'lon joylash"),
    BotCommand(command="get_adver", description="Barcha e'lonlar"),
    BotCommand(command="clearad", description="Barcha reklamalarni o'chirish"),
    BotCommand(command="clearpupil", description="Barcha o'quvchilarni o'chirish")
]
user_commands = [
    BotCommand(command="start", description="Qayta ishga tushirish"),
    BotCommand(command='help', description="Bot haqida"),
    BotCommand(command='register', description="Ro'yhatdan o'tish")
]


admins = [6004455264]
@command_router.message(CommandStart())
async def start_handler(message: Message):
    if message.from_user.id in admins:
        await message.bot.set_my_commands(commands=admin_commands)
        await message.answer(text="Hurmatli admin, Hush kelibsiz!")
    else:
        await message.bot.set_my_commands(commands=user_commands)
        await message.answer(text=f"Assalomu Alaykum, <b>{message.from_user.first_name}</b>!\n\nBotimizga hush kelibsiz 🥳🥳🥳\nBu bot orqali Arab Tili kursimizga yozilishingiz mumkin ✅✅✅\n\nBatafsil ma'lumot uchun /help ni bosing.")
    
@command_router.message(Command('help'))
async def help_handler(message: Message):
    await message.answer(
        text="Assalomu Alaykum, Hurmatli o'quvchi 👋\n\nBizning arab tili kurslarimizni tanlaganingizdan mamnunmiz 😃\nAtigi  100 ming so'm evasiga siz Arab tili 0 dan boshlab\nOqish Yozish Arab tili fonetikasi\nArab tili grammatikasi Arab tilida sozlashishni mukammal o'zlashtirishingiz mumkin ✔✔✔\nSiz kurslarimiz davomida Arab Tilini tajribali ustozlar tomonidan \ntez va sifatli o'rganasiz 😉😉😉\n\nKursga yozilish uchun /register linkni bosing 👇"
    )

@command_router.message(Command('pupils'))
async def users_handler(message: Message):
    users = db.get_users()
    if len(users) >= 1:
        for user in users:
            await message.answer_photo(
                photo=user[5],
                caption=f"\n👤  To'liq ismi: <b>{user[0]} {user[1]}</b>\n👥  Yoshi: {user[2]}\n\n📆  Kun: {user[6]}\n⏰  Vaqt: {user[7]}\n\n📍 Manzil: {user[3]}\n📲  Telefon raqami: {user[4]}\n\n"
            )
    else:
        await message.answer(
            text="Hozircha hech qanday o'quvchilar yo'q. 🧐🧐🧐"
        )

@pupil_router.message(Command('register'))
async def register_handler(message: Message, state: FSMContext):
    await message.answer(
        text="Iltimos, ismingizni kiriting..."
    )
    await state.set_state(PupilStates.first_name_state)

@pupil_router.message(PupilStates.first_name_state)
async def first_name_handler(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(PupilStates.last_name_state)
    await message.answer(
        text="Yaxshi, iltimos familiyangizni kiriting..."
    )

@pupil_router.message(PupilStates.last_name_state)
async def last_name_handler(message: Message, state: FSMContext):
    await state.update_data(lname = message.text)
    await state.set_state(PupilStates.age_state)
    await message.answer(
        text="Yaxshi, iltimos yoshingizni kiriting..."
    )

@pupil_router.message(PupilStates.age_state)
async def age_handler(message: Message, state:FSMContext):
    await state.update_data(age = message.text)
    await state.set_state(PupilStates.address_state)
    await message.answer(
        text="Yaxshi, iltimos manzilingizni yuboring...\nMasalan(Mustaqillik MFY, Mingbodom ko'chasi, 15-uy)"
    )

@pupil_router.message(PupilStates.address_state)
async def adres_handler(message: Message, state: FSMContext):
    await state.update_data(adres = message.text)
    await state.set_state(PupilStates.phone_state)
    await message.answer(
        text="Yaxshi, iltimos raqamingizni '+9989012345678' formatda kiriting..."
    )

day_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Dushanba-Chorshanba-Juma"),
            KeyboardButton(text="Seshanba-Payshanba-Shanba")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
time_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Kunning birinchi yarmi (8:00 - 12:00 oraliq)"),
            KeyboardButton(text="Kunning ikkinchi yarmi (13:00 - 21:00 oraliq)")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

@pupil_router.message(PupilStates.phone_state)
async def number_handler(message: Message, state: FSMContext):
    await state.update_data(phone = message.text)
    await state.set_state(PupilStates.day_state)
    await message.answer(
        text="Yaxshi, iltimos sizga maqul kunni tanlang...",
        reply_markup=day_kb
    )

@pupil_router.message(PupilStates.day_state)
async def day_handler(message: Message, state: FSMContext):
    await state.update_data(day = message.text)
    await state.set_state(PupilStates.time_state)
    await message.answer(
        text="Yaxshi, iltimos o'zingizga maqul vaqtni tanlang...",
        reply_markup=time_kb
    )

@pupil_router.message(PupilStates.time_state)
async def time_handler(message: Message, state: FSMContext):
    await state.update_data(time = message.text)
    await state.set_state(PupilStates.image_state)
    await message.answer(
        text="Yaxshi, iltimos rasmingizni kiriting...",
        reply_markup=ReplyKeyboardRemove()
    )

@pupil_router.message(PupilStates.image_state)
async def image_handler(message: Message, state: FSMContext):
    await state.update_data(image = message.photo[-1].file_id)
    all_data = await state.get_data()
    if message.photo:
        await message.answer_photo(
            photo=all_data.get('image'),
            caption=f"Ismi: <b>{all_data.get('name')}</b>\nFamiliyasi: {all_data.get('lname')}\nYoshi: {all_data.get('age')}\nManzil: {all_data.get('adres')}\nTelefon raqami: {all_data.get('phone')}\nKurs vaqti: {all_data.get('time')}\nKun: {all_data.get('day')}"
        )
        all_data = await state.get_data()
        db.add_user(
            name=all_data.get('name'),
            lname=all_data.get('lname'),
            age=all_data.get('age'),
            phone=all_data.get('phone'),
            adres=all_data.get('adres'),
            image=all_data.get('image'),
            times=all_data.get('time'),
            day=all_data.get('day'),
            owner_id=message.from_user.id 
        )
        await message.answer("Muvaffaqqiyatli yuborildi", parse_mode=ParseMode.HTML)
        await state.clear()
    else:
        await message.answer("Iltimos, rasm yuboring.")

adver_router = Router()

@pupil_router.message(Command("clearad"))
async def adver_delete(message: Message):
    db.del_from("advertisiments")
    await message.answer(
        text="Reklamalar ro'yhati muvaffaqqiyatli o'chirildi"
    )

@pupil_router.message(Command('clearpupil'))
async def pupil_delete_handler(message: Message):
    db.del_from('pupils')
    await message.answer(
        text="O'quvchilar ro'yhati muvaffaqqiyatli o'chirildi"
    )


@adver_router.message(Command('advertisiment'))
async def add_adver_handler(message: Message, state: FSMContext):
    await state.set_state(AdverState.adver_state)
    await message.answer(
        text="Iltimos, E'lon uchun sarlavha kiriting..."
    )

@adver_router.message(AdverState.adver_state)
async def adver_title_handler(message: Message, state: FSMContext):
    await state.update_data(advertitle = message.text)
    await state.set_state(AdverState.adver_desc)
    await message.answer(
        text="Yaxshi, E'lon uchun matn kiriting..."
    )

@adver_router.message(AdverState.adver_desc)
async def adver_text_handler(message: Message, state:FSMContext):
    await state.update_data(advertext = message.text)
    await state.set_state(AdverState.adver_img)
    await message.answer(
        text="Yaxshi, E'lon rasmini kiriting..."
    )

@adver_router.message(AdverState.adver_img)
async def adver_img_handler(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(adverimg=message.photo[-1].file_id)
        all_data = await state.get_data()

        adver_title = all_data.get('advertitle')
        adver_text = all_data.get('advertext')
        adver_image = all_data.get('adverimg')

        # Barcha foydalanuvchilarga e'lonni jo'natish
        users = db.get_users()  # Barcha foydalanuvchilarni olish
        for user in users:
            user_id = user[8]  # Foydalanuvchi ID'sini olish
            await bot.send_photo(
                chat_id=user_id,
                photo=adver_image,
                caption=f"{adver_title}\n\n{adver_text}"
            )

        # E'lonni bazaga qo'shish
        db.add_adver(
            name=adver_title,
            desc=adver_text,
            image=adver_image
        )

        # Foydalanuvchilarga e'lonni qo'shish haqida xabar yuborish
        await message.answer(text="E'lon muvaffaqiyatli barcha foydalanuvchilarga jo'natildi.")

        # Holatni tozalash
        await state.clear()

@pupil_router.message(Command('cources'))
async def course_handler(message: Message):
    await message.answer(
        text="Kurslarimiz "
    )

@adver_router.message(Command('get_adver'))
async def adver_handler(message: Message):
    advertisiment = db.get_adver()
    if len(advertisiment) > 0:
        for ad in advertisiment:
            await message.answer_photo(
                photo=ad[2],
                caption=f"<b>{ad[0]}</b>\n\n{ad[1]}"
            )
    else:
        await message.answer(
            text="Hozircha e'lonlar yo'q."
        )


        
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
async def main():
    
    dp = Dispatcher()
    dp.include_routers(command_router, pupil_router, adver_router)
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")

