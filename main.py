from flask import Flask
from uuid import uuid4
from library import parsing_data, send_message, \
                    adding_a_dog, working_with_command, \
                    changing_a_dog, looking_for_a_dog


app = Flask(__name__)
users_dogs = {

    '8c42f59f-33bd-42d7-a2bc-75e5dcec610b': {
        'breed': 'dvorniaga',
        'name': 'Ben',
    },

    '8c42f59f-33bd-42d7-a2bc-75e5dcec610a': {
        'breed': 'terrier',
        'name': 'Gari',
    },

    'ecd5de1b-f264-4f2c-880d-0c75b80e02c1': {
        'breed': 'Dachshund',
        'name': 'Lili',
    }
}


@app.route('/', methods=['POST'])
def index() -> dict:
    data = parsing_data()
    if data['text'] == '/start':
        data['text'] = 'Доступные комманды:' \
                       '\n /dogs,' \
                       ' \n/add_dog name breed,' \
                       ' \n/del_dog name, ' \
                       ' \n/change_info old_name new_breed new_name'
        send_message(data)
        return data
    elif data['text'] == '/dogs':
        data['text'] = str(users_dogs)
        send_message(data)
        return data
    elif working_with_command(data['text'])[0] == '/add_dog':
        new_dog = adding_a_dog(working_with_command(data['text']))
        if new_dog != {}:
            users_dogs[str(uuid4())] = new_dog
            data['text'] = 'Собака успешно добавлена!'
            send_message(data)
            return new_dog
        data['text'] = 'Не хватает аргументов'
        send_message(data)
        return users_dogs
    elif working_with_command(data['text'])[0] == '/del_dog':
        info = working_with_command(data['text'])
        name = info[1]
        user_dog_id = looking_for_a_dog(data=users_dogs, name=name)
        try:
            if user_dog_id != 'Такой собаки нет(':
                del users_dogs[user_dog_id]
                data['text'] = 'Собака успешно удалена!'
                send_message(data)
                return users_dogs
        except KeyError:
            data['text'] = 'Такой собаки нет('
            send_message(data)
    elif working_with_command(data['text'])[0] == '/change_info':
        info = working_with_command(data['text'])
        old_name = info[1]
        user_dog_id = looking_for_a_dog(data=users_dogs, name=old_name)
        try:
            if user_dog_id != 'Такой собаки нет(':
                user_dog = changing_a_dog(info)
                if user_dog != {}:
                    users_dogs[user_dog_id] = user_dog
                    data['text'] = 'Информация о собаке изменена!'
                    send_message(data)
                    return user_dog
                elif user_dog == {}:
                    data['text'] = 'Не хватает аргументов'
                    send_message(data)
        except KeyError:
            data['text'] = 'Такой собаки нет('
            send_message(data)
    return data


if __name__ == '__main__':
    app.run(port=443, ssl_context='adhoc')

