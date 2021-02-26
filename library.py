import requests
from requests import Response
from flask import request

url = 'https://api.telegram.org/bot1678177422:AAFAOiyRFhiIN6yFa2SeBleOaoQjnm9aeJ0/'


def send_message(data: dict) -> Response:
    """Отправка сообщения"""
    message = requests.post(url=url + 'sendMessage', data=data)
    return message


def parsing_data() -> dict:
    """Обработка json файла"""
    message_info = request.get_json()
    message = message_info['message']
    chat_info = message['chat']
    chat_id = chat_info['id']
    try:
        text = message['text']
    except KeyError:
        text = 'Я этого не понимаю('
    data = {'chat_id': chat_id, 'text': text}
    return data


def adding_a_dog(data: list) -> dict:
    """Создание информации по собаке"""
    try:
        breed = data[1]
        name = data[2]
        new_dog = {'breed': breed, 'name': name}
        return new_dog
    except IndexError:
        new_dog = {}
        return new_dog


def working_with_command(command_text: str) -> list:
    """Разделение строки для выделения команды"""
    text = command_text.split()
    return text


def changing_a_dog(data: list) -> dict:
    """Изменение инфы собаки"""
    try:
        new_breed = data[2]
        new_name = data[3]
        user_dog = {'breed': new_breed, 'name': new_name}
        return user_dog
    except IndexError:
        user_dog = {}
        return user_dog


def looking_for_a_dog(data: dict, name: str):
    """Поиск собаки"""
    try:
        for user_dog_id, dog in data.items():
            if dog['name'] == name:
                return user_dog_id
    except KeyError:
        return 'Такой собаки нет('
