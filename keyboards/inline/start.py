import os

from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile
from aiogram.types import (
    Message
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pytube import YouTube

from keyboards.base import common_keyboard
from services.youtube_downloader import download_youtube_video, printVideo_res

start_router = Router()


class Form(StatesGroup):
    go_download_video_menu2 = State()
    go_download_video_menu21 = State()
    go_download_video_menu3 = State()


@start_router.message(CommandStart())
async def start(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text='Youtube downloader', callback_data='Youtube downloader')
    builder.adjust(1)
    await message.answer("Виибирай інструмент: ", reply_markup=builder.as_markup())


@start_router.callback_query(F.data == "Youtube downloader" or Command('/cancelDownloadyt'))
async def yt_downloader_menu(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="Завантажити відео", callback_data='Download video')
    await callback.message.answer("Вибери дію", reply_markup=builder.as_markup())


@start_router.callback_query(F.data == "Download video")
async def download_video_menu(message: Message, state: FSMContext):
    await state.set_state(Form.go_download_video_menu2)
    await message.message.answer('Щоб скасувати - <b>/cancelDownloadyt</b>\n'
                                 'Надішліть мені посилання на відео: ')


@start_router.message(Form.go_download_video_menu2)
async def download_video_menu2(message: Message, state: FSMContext):
    if message.text.startswith("youtube"):
        link = 'https://www.' + message.text
        await state.update_data(link=link)
        info = await state.get_data()
        link = info['link']

        await state.set_state(Form.go_download_video_menu21)
        result = printVideo_res(link)
        await message.answer('Виберіть <b>якість</b> якою скачати відео.',
                             reply_markup=common_keyboard(*result))
        await state.update_data(result=result)
    elif message.text.startswith("https://www.youtube"):
        await state.update_data(link=message.text)
        info = await state.get_data()
        link = info['link']

        await state.set_state(Form.go_download_video_menu21)
        result = printVideo_res(link)
        await message.answer('Виберіть <b>якість</b> якою скачати відео.',
                             reply_markup=common_keyboard(*result))
        await state.update_data(result=result)
    else:
        await message.answer("Це не посилання на відео з <b>Ютуб</b>")


@start_router.message(Form.go_download_video_menu21)
async def download_video_menu21(message: Message, state: FSMContext):
    await state.update_data(rs=message.text)
    await state.set_state(Form.go_download_video_menu3)


@start_router.message(Form.go_download_video_menu3)
async def download_video_menu3(message: Message, state: FSMContext):
    info = await state.get_data()
    yt = YouTube(info['link'])
    if info['rs'] in info['result']:
        await message.answer(f"Завантаження відео: {yt.title}")
        download_youtube_video(info['link'], info['rs'])
        # Отправка файла из файловой системы
        await message.answer("Завантаження відео завершено!")
        await message.answer("Відсилання відео")
        title = "".join(c for c in yt.title if c.isalpha())
        output_path = "services/temp_videos/" + title + ".mp4"
        image_from_pc = FSInputFile(path=output_path, filename='temp_videos')
        await message.answer_video(
            image_from_pc,
            caption=f"Заголовок: {yt.title}\n"
                    f"Автор: {yt.author}\n"
                    f"Якість: {info['rs']}")
        os.remove(output_path)
    else:
        await message.answer('Я вас не розумію')
    await state.clear()
