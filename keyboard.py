from turtle import width
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import material


langs = ReplyKeyboardMarkup(resize_keyboard=True).add('Toshkent viloyati', 'Andijon viloyati',
'Buxoro viloyati', 'Farg\'ona viloyati', 'Jizzax viloyati', 'Xorazm viloyati', 'Namangan viloyati', 'Navoiy viloyati',
'Qashqadaryo viloyati', 'Qoraqalpog\'iston viloyati', 'Samarqand viloyati', 'Sirdaryo viloyati', 'Surxandaryo viloyati')

menu = ReplyKeyboardMarkup(resize_keyboard= True).add('VILOYAT TANLASH', 'HA')


a = InlineKeyboardButton('Delete', callback_data='delete')
delete = InlineKeyboardMarkup().add(a)
