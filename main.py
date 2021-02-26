from flask import Flask
from library import parsing_data, send_message, \
                    working_with_command, delete_dog, \
                    show_all_dogs, add_new_dog, \
                    changing_info_about_dog


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
        show_all_dogs(data=data, data_base=users_dogs)
    elif working_with_command(data['text'])[0] == '/add_dog':
        add_new_dog(data=data, data_base=users_dogs)
    elif working_with_command(data['text'])[0] == '/del_dog':
        delete_dog(data=data, data_base=users_dogs)
    elif working_with_command(data['text'])[0] == '/change_info':
        changing_info_about_dog(data=data, data_base=users_dogs)
    return data


if __name__ == '__main__':
    app.run(port=443, ssl_context='adhoc')

