import asyncio

import aiogram.types
from aiogram.utils import executor

import tictokAPI
from config import *
from helper import check_link
from loader import dp, bt, debug_run, run_mode, logger
from tictokAPI import Downloader


@dp.message_handler()
async def tg_download(message: aiogram.types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("<i>Привет! Я чат-бот, разработанный для личного использования моим создателем."
                             " К сожалению, я не предназначен для общего публичного использования.\n\n"
                             "Hello! I am a chatbot designed for personal use by my creator."
                             " Unfortunately I am not intended for general public use.</i>\n<code>.te</code>",
                             parse_mode="HTML")
        logger.info(f"[TG] - Trying to use the bot by another user |"
                    f" User:{message.from_user.id} ({message.from_user.username})")
        return

    checked_url = check_link(message.text)
    if checked_url:
        resp = await message.answer("<i>⬇️ Начало загрузки видео...</i>", parse_mode="HTML")
        try:
            v = Downloader.download(checked_url)
        except tictokAPI.FailedDownload:
            await resp.edit_text("<i>Ошибка загрузки, повторите попытку позже</i>", parse_mode="HTML")
            logger.critical("[TG] - failed to download the video")
        else:
            logger.debug(f"Video Info: {v}")
            await resp.edit_text("🔄 Отправка видео..", parse_mode="HTML")
            with open(v.filename, "rb") as f:
                video = await bt.send_video(
                    chat_id=message.from_user.id,
                    video=f
                )
            await resp.delete()
            await video.edit_caption("<code>.te</code>", parse_mode="HTML")
            logger.success(f"[TG] - Success send to {message.from_user.id} ({message.from_user.username})")
            await delete_file(v.filename)
    else:
        await message.answer("<i>Некорректная ссылка!</i>", parse_mode="HTML")
        logger.info(f"[TG] - incorrect link ({message.text}) |"
                    f" User: {message.from_user.id} ({message.from_user.username}) ")


async def delete_file(path: str):
    logger.debug(f"[CLEAN] - The file will be deleted in a minute \"{path}\"")
    await asyncio.sleep(60)
    os.remove(path)
    logger.debug(f"[CLEAN] - Delete file \"{path}\"")


async def on_startup(_):
    """
    Действие при запуске бота.
    """
    if not os.path.exists("./temp"):
        os.mkdir("temp")

    if run_mode():
        await bt.set_webhook(WEBHOOK_URL)
    logger.success('[BOT] Бот запущен!')


async def on_shutdown(_):
    """
    Действие при остановке бота.
    """
    ...
    if run_mode():
        await bt.delete_webhook()
    logger.critical('[BOT] Бот остановлен!!!')


if __name__ == '__main__':
    if not debug_run():
        # Проверка на root
        if os.getuid() != 0:
            logger.critical('Необходим запуск от имени суперпользователя')
            exit()
    if run_mode():
        logger.debug('[BOT] Запуск в режиме WEBHOOK')
        executor.start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT
        )
    else:
        logger.debug('[BOT] Запуск в режиме POLLING')
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
