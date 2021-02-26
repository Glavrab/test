import requests
from requests import Response
from flask import request
from uuid import uuid4
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


def show_all_dogs(data: dict, data_base: dict) -> dict:
    data['text'] = str(data_base)
    send_message(data)
    return data


def add_new_dog(data: dict, data_base: dict) -> None:
    new_dog = adding_a_dog(working_with_command(data['text']))
    if new_dog != {}:
        data_base[str(uuid4())] = new_dog
        data['text'] = 'Собака успешно добавлена!'
        send_message(data)
        return
    data['text'] = 'Не хватает аргументов'
    send_message(data)


def delete_dog(data: dict, data_base: dict) -> None:
    info = working_with_command(data['text'])
    name = info[1]
    user_dog_id = looking_for_a_dog(data=data_base, name=name)
    try:
        if user_dog_id != 'Такой собаки нет(':
            del data_base[user_dog_id]
            data['text'] = 'Собака успешно удалена!'
            send_message(data)
    except KeyError:
        data['text'] = 'Такой собаки нет('
        send_message(data)


def changing_info_about_dog(data: dict, data_base: dict) -> None:
    info = working_with_command(data['text'])
    old_name = info[1]
    user_dog_id = looking_for_a_dog(data=data_base, name=old_name)
    try:
        if user_dog_id != 'Такой собаки нет(':
            user_dog = changing_a_dog(info)
            if user_dog != {}:
                data_base[user_dog_id] = user_dog
                data['text'] = 'Информация о собаке изменена!'
                send_message(data)
            elif user_dog == {}:
                data['text'] = 'Не хватает аргументов'
                send_message(data)
    except KeyError:
        data['text'] = 'Такой собаки нет('
        send_message(data)
