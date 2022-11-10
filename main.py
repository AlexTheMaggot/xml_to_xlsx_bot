from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup as Bs
import pandas as pd
from config import API_TOKEN


def xml_to_xlsx(file):
    xml_doc = open(file, 'r')
    soup = Bs(xml_doc, 'xml')
    message = soup.find_all('MESSAGE')
    data = []
    for i in message:
        data_item = {
            'datetime': i.attrs['TIME'],
            'priority': i.PRIORITY.contents[0],
            'sign': i.SIGN.contents[0],
            'textnb': i.TEXTNB.contents[0],
        }
        if i.find('TEXT'):
            data_item['text'] = i.TEXT.contents[0]
        else:
            data_item['text'] = None
        data.append(data_item)

    table = pd.DataFrame(data)
    table.to_excel('upload.xlsx')


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply('Приветствую! Для работы бота отправьте файл .xml и он пришлет файл .xlsx')


@dp.message_handler(content_types=['document'])
async def file_echo(message: types.Message):
    await message.reply('Обработка файла...')
    await message.document.download(destination_file='./download.xml')
    xml_to_xlsx('./download.xml')
    await message.reply_document(open('upload.xlsx', 'rb'), caption='Готово!')


if __name__ == '__main__':
    executor.start_polling(dp)
