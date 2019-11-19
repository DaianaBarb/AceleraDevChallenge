import hashlib

import requests
import json
import os

TOKEN = os.getenv('TOKEN')
RECEIVE_API_URL = 'https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token={}'.format(TOKEN)
SEND_API_URL = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token={}'.format(TOKEN)
ANSWER_JSON_FILE = '.../files/answer.json'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def handle_message():
    origin_message = get_message()
    save_message(origin_message)

    decrypted_text = decrypt_message_caesar_cipher(origin_message['numero_casas'], origin_message['cifrado'])
    update_message('decifrado', decrypted_text)

    summary = encrypt_message_sha1(decrypted_text)
    update_message('resumo_criptografico', summary)

    send_message()


def get_message():
    try:
        response = requests.get(url=RECEIVE_API_URL)
        return json.loads(response.text)
    except Exception as e:
        print(e)


def save_message(message):
    arquivo = open('answer.json', 'w')
    arquivo.write(json.dumps(message))


def decrypt_message_caesar_cipher(key, ciphertext):
    ciphertext = ciphertext.upper()
    decrypted_message = ''
    for letter in ciphertext:
        index = ALPHABET.find(letter)
        index = (index - key) % 26
        if letter in ALPHABET:
            decrypted_message = decrypted_message + ALPHABET[index]
        elif letter == " ":
            decrypted_message = decrypted_message + " "
        else:
            decrypted_message = decrypted_message + letter

    return decrypted_message.lower()


def encrypt_message_sha1(decrypted_text):
    return hashlib.sha1(decrypted_text.encode('utf-8')).hexdigest()


def update_message(info, updated_info):
    with open('answer.json') as f:
        content = f.readlines()
    message = json.loads(content[0])
    message[info] = updated_info
    save_message(message)


def send_message():
    pass


if __name__ == '__main__':
    handle_message()
