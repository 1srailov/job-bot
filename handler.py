from distutils.command.config import config
import json
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import executor

import material
import keyboard

from database.database import Database
from bot import *


db = Database()
count = 0
city = ''


@dp.message_handler(commands=["start"])
async def language(msg: Message):
    
    if msg.from_user.id == admin_id:
        await msg.answer("Welcome admin!")
        return

    await msg.answer("Siz qaysi viloyatdan ish izlayapsiz?", reply_markup=keyboard.langs)



@dp.message_handler()
async def menus(msg: Message):
    global count, city
    print(count)
    if msg.text in list(material.viloyatlar.keys()):
        city = material.viloyatlar.get(msg.text)
        values = await db.get_job(city)
        if(len(values) != 0):
            for i in values:
                try:
                    await msg.answer_photo(open(f'image/{i[3]}', 'rb'), i[2])
                except:
                    await msg.answer(i)
                    await msg.answer(i[2])

                count += 1

                if(count % 10 == 0):
                    await msg.answer("Korishni davom etasizmi?", reply_markup= keyboard.menu)
                    break

            if count < 10:
                count = 0

                    
        
        else:
            await msg.answer("bu viloyatda hozirchalik ish yoq")

    if msg.text == 'HA':
        limit = 0
        values = await db.get_job(city)
        if count + 10 > len(values):
            limit = len(values)

        if len(values) - count <= 0:
            await msg.answer("hozirchalik shu...")

        else:
            limit = count + 10
        for i in values[count:limit]:
            try:
                await msg.answer_photo(open(f'image/{i[3]}', 'rb'), i[2])
            except:
                await msg.answer(i)
                await msg.answer(i[2])

            count += 1
            if(count % 10 == 0):
                    await msg.answer("Korishni davom etasizmi?", reply_markup= keyboard.menu)
                    break


    if msg.text == 'VILOYAT TANLASH': 
        await msg.answer("Iltimos viloyatni tanlang:", reply_markup=keyboard.langs)
        count = 0





@dp.channel_post_handler(content_types=['photo'])
async def channel_post_handler(msg:Message):
            for i in list(material.heshtegs.keys()):
                if i in msg.caption:
                    file = await msg.photo[-1].get_file() 
                    a = await file.download(destination_file= f"image/{msg.message_id}.jpg")
                    await db.add_job(material.heshtegs.get(i), msg.caption, f'{msg.message_id}.jpg')
                    await bot.send_photo(admin_id, open(f'image/{msg.message_id}.jpg', 'rb'), msg.caption, reply_markup= keyboard.delete)
                    break



@dp.callback_query_handler()
async def process_callback_kb1btn1(callback_query:CallbackQuery):
    await db.delete_job(callback_query.message.caption)
    await bot.send_message(admin_id, "muvaqqiyatli ochirildi")
               
              
#     image_accept = await db.get_image_accept(user_id)

#     if image_accept:
#         await bot.send_photo(admin_id, msg.photo[len(msg.photo) - 1].file_id)
#         await bot.send_message(admin_id, user_id)

#         await db.update_image_accept(False, user_id)


if __name__ == "__main__":
    print("Started")

    executor.start_polling(dp)
