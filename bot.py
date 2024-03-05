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
BOT_TOKEN = "7193192692:AAHVkhg7uVzsI5c43qbyZ6EOl7-nxhM51eQ"




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
    

    def add_user(self, name, lname, age, adres, phone, owner_id, day, times):
        self.cursor.execute(
            "INSERT INTO pupils (phone, f_name, l_name, age, adress, owner, day, times) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", (phone, name, lname,age, adres, owner_id, day, times)
        )
        self.conn.commit()

    def get_users(self):
        self.cursor.execute(
            "SELECT f_name, l_name, age, adress, phone, image, day, times, owner FROM pupils;"
        )        
        result = self.cursor.fetchall()
        return result
    
    def check_user(self, owner_id):
        self.cursor.execute(
            "SELECT * FROM pupils WHERE owner = ?;", (owner_id,)
        )
        res = self.cursor.fetchall()
        return res
    
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
    BotCommand(command="clearpupil", description="Barcha o'quvchilarni o'chirish"),
    BotCommand(command="cancel", description="Bajarilayotgan ishni bekor qilish")
]
user_commands = [
    BotCommand(command="start", description="Qayta ishga tushirish"),
    BotCommand(command='help', description="Bot haqida"),
    BotCommand(command="news", description="Yangiliklar oynasi"),
    BotCommand(command='register', description="Ro'yhatdan o'tish"),
    BotCommand(command="cancel", description="Bajarilayotgan ishni bekor qilish")
]

# 6004455264,1908438933,973895268
admins = [6004455264,1908438933,973895268]
@command_router.message(CommandStart())
async def start_handler(message: Message):
    user_tel = message.from_user.id
    if user_tel in admins:
        await message.answer(text="Hurmatli admin, Hush kelibsiz!")
        await bot.set_my_commands(commands=admin_commands)
        await message.answer(
            text="/start - Botni ishga tushirish uchun\n/pupils - Kursga yozilganlar\n/advertisiment - E'lon joylash\n/get_adver - Barcha e'lonlar\n/clearad - Barcha reklamalarni o'chirish\n/clearpupil - Barcha o'quvchilarni o'chirish"
        )
    else:
        await bot.set_my_commands(commands=user_commands)
        await message.answer(text=f"Assalomu Alaykum, <b>{message.from_user.first_name}</b>!\n\nBotimizga hush kelibsiz 🥳🥳🥳\nBu bot orqali Arab Tili kursimizga yozilishingiz mumkin ✅✅✅\n\nBatafsil ma'lumot uchun /help ni bosing yoki ro'yhatdan o'tish uchun /register ni bosing.")
    
@command_router.message(Command('help'))
async def help_handler(message: Message):
    await message.answer(
        text="Assalomu Alaykum, Hurmatli o'quvchi 👋\n\nBizning arab tili kurslarimizni tanlaganingizdan mamnunmiz 😃\nAtigi  100 ming so'm evasiga siz Arab tili 0 dan boshlab\nOqish Yozish Arab tili fonetikasi\nArab tili grammatikasi Arab tilida sozlashishni mukammal o'zlashtirishingiz mumkin ✔✔✔\nSiz kurslarimiz davomida Arab Tilini tajribali ustozlar tomonidan \ntez va sifatli o'rganasiz 😉😉😉\n\nKursga yozilish uchun /register linkni bosing 👇"
    )

@command_router.message(Command('cancel'))
async def cancel_handler(message: Message, state: FSMContext):
    await message.answer(text="Bajarilayotgan amallar bekor qilindi")
    await state.clear()

@command_router.message(Command('pupils'))
async def users_handler(message: Message):
    user_tel = message.from_user.id
    if user_tel in admins:
        users = db.get_users()
        if len(users) >= 1:
            for user in users:
                await message.answer(
                    # photo=user[5],
                    text=f"\n👤  To'liq ismi: <b>{user[0]} {user[1]}</b>\n👥  Yoshi: {user[2]}\n\n📆  Kun: {user[6]}\n⏰  Vaqt: {user[7]}\n\n📍 Manzil: {user[3]}\n📲  Telefon raqami: {user[4]}\n\n"
                )
        else:
            await message.answer(
                text="Hozircha hech qanday o'quvchilar yo'q. 🧐🧐🧐"
            )
    else:
        await message.answer(
            text='Hurmatli foydalanuvchi, siz bu buyruqdan foydalana olmaysiz ❌❌❌'
        )

@pupil_router.message(Command('register'))
async def register_handler(message: Message, state: FSMContext):
    user_tel = message.from_user.id
    if user_tel not in admins:
        res = db.check_user(user_tel)
        if res:
            await message.answer(text="Hurmatli foydalanuvchi, siz allaqachon ro'yhatdan o'tgansiz. Iltimos adminlarimiz javobini kuting.")
        else:
            await message.answer(
                text="Iltimos, ismingizni kiriting..."
            )
            await state.set_state(PupilStates.first_name_state)
    else:
        await message.answer(text='Hurmatli admin, siz bu buyruqdan foydalana olmaysiz ❌❌❌')

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

contact_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Raqamni yuborish", request_contact=True)
        ]
    ],
    resize_keyboard=True
)

@pupil_router.message(PupilStates.address_state)
async def adres_handler(message: Message, state: FSMContext):
    await state.update_data(adres = message.text)
    await state.set_state(PupilStates.phone_state)
    await message.answer(
        text="Yaxshi, iltimos pastdagi Raqamni yuborish tugmasini bosing...",
        reply_markup=contact_kb
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
    if message.contact:    
        await state.update_data(phone = message.contact.phone_number)
        await state.set_state(PupilStates.day_state)
        await message.answer(
            text="Yaxshi, iltimos sizga maqul kunni tanlang...",
            reply_markup=day_kb
        )
    else:
        await state.set_state(PupilStates.phone_state)
        await message.answer(text="Iltimos Raqamni yuborish tugmasini bosing...")

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
    all_data = await state.get_data()
    if message.text:
        await message.answer(
            text=f"Ismi: <b>{all_data.get('name')}</b>\nFamiliyasi: {all_data.get('lname')}\nYoshi: {all_data.get('age')}\nManzil: {all_data.get('adres')}\nTelefon raqami: {all_data.get('phone')}\nKurs vaqti: {all_data.get('time')}\nKun: {all_data.get('day')}"
        )
        all_data = await state.get_data()
        db.add_user(
            name=all_data.get('name'),
            lname=all_data.get('lname'),
            age=all_data.get('age'),
            phone=str(all_data.get('phone')),
            adres=all_data.get('adres'),
            times=all_data.get('time'),
            day=all_data.get('day'),
            owner_id=message.from_user.id 
        )
        await message.answer("Muvaffaqqiyatli yuborildi", parse_mode=ParseMode.HTML)
        await state.clear()
    else:
        await message.answer("Yaxshi, iltimos o'zingizga maqul vaqtni tanlang..")
        await state.set_state(PupilStates.time_state)


adver_router = Router()

@pupil_router.message(Command("clearad"))
async def adver_delete(message: Message):
    user_tel = message.from_user.id
    if user_tel in admins:
        db.del_from("advertisiments")
        await message.answer(
            text="Reklamalar ro'yhati muvaffaqqiyatli o'chirildi"
        )
    else:
        await message.answer(text='Hurmatli foydalanuvchi, siz bu buyruqdan foydalana olmaysiz ❌❌❌')

@pupil_router.message(Command('clearpupil'))
async def pupil_delete_handler(message: Message):
    user_tel = message.from_user.id
    if user_tel in admins:
        db.del_from('pupils')
        await message.answer(
            text="O'quvchilar ro'yhati muvaffaqqiyatli o'chirildi"
        )
    else:
        await message.answer(text='Hurmatli foydalanuvchi, siz bu buyruqdan foydalana olmaysiz ❌❌❌')

@adver_router.message(Command('advertisiment'))
async def add_adver_handler(message: Message, state: FSMContext):
    user_tel = message.from_user.id
    if user_tel in admins:
        await state.set_state(AdverState.adver_state)
        await message.answer(
            text="Iltimos, E'lon uchun sarlavha kiriting..."
        )
    else:
        await message.answer(text='Hurmatli foydalanuvchi, siz bu buyruqdan foydalana olmaysiz ❌❌❌')

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


@adver_router.message(Command('get_adver'))
async def adver_handler(message: Message):
    user_tel = message.from_user.id
    if user_tel in admins:
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

    else:
        await message.answer(text='Hurmatli foydalanuvchi, siz bu buyruqdan foydalana olmaysiz ❌❌❌')



@adver_router.message(Command('news'))
async def news_handler(message: Message):
    user_tel = message.from_user.id
    if user_tel not in admins:
        advertisiment = db.get_adver()
        if len(advertisiment) > 0:
            for ad in advertisiment:
                await message.answer_photo(
                    photo=ad[2],
                    caption=f"<b>{ad[0]}</b>\n\n{ad[1]}"
                )
        else:
            await message.answer(
                text="Hozircha yangiliklar yo'q."
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

