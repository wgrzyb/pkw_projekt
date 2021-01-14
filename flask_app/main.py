import json
import os
import uuid

import requests
from algosdk import transaction
from flask import Flask, render_template, request, flash
from werkzeug.utils import redirect, secure_filename
from algosdk.v2client import algod

from flask_app.config import Config

app = Flask(__name__, static_url_path=Config.flask_static_url_path)
app.config.from_object('config.BaseConfig')


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Strona główna')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.allowed_extensions


# Function from Algorand Inc.
def wait_for_confirmation(client, tx_id):
    last_round = client.status().get('last-round')
    tx_info = client.pending_transaction_info(tx_id)
    while not (tx_info.get('confirmed-round') and tx_info.get('confirmed-round') > 0):
        print('Czekanie na potwierdzenie transakcji...')
        last_round += 1
        client.status_after_block(last_round)
        tx_info = client.pending_transaction_info(tx_id)
    print(f"Transakcja potwierdzona w turze: {tx_info.get('confirmed-round')}")
    return tx_info


def share_file(files):
    # Dodawanie pliku do ipfs-a
    print("Dodawanie pliku do IPFS-a.")
    url = f"{Config.ipfs_api_address}/api/v0/add"
    params = (('wrap-with-directory', True),)
    response = requests.post(url, files=files, params=params)
    if response.status_code != 200:
        print(response.text)
        raise Exception(f"Invalid status code: '{response.status_code}'.")
    result = response.text.splitlines()
    cid = json.loads(result[1]).get('Hash')
    print("Plik dodano do IPFS-a.")
    # Dodawanie informacji do blockchain-a Algorand
    print("Dodawanie informacji do blockchain-a Algorand.")
    algod_token = Config.algod_token
    algod_address = Config.algod_api_address
    purestake_token = {'X-Api-key': algod_token}
    algod_client = algod.AlgodClient(algod_token, algod_address, headers=purestake_token)
    # ustawienie parametrów transakcji
    params = algod_client.suggested_params()
    gh = params.gh
    first_valid_round = params.first
    last_valid_round = params.last
    fee = params.min_fee
    send_amount = 0
    note = f"{{'cid': {cid}}}".encode()
    sender = Config.algod_public_key
    receiver = Config.algod_public_key
    # utworzenie i zatwierdzenie transakcji
    tx = transaction.PaymentTxn(sender, fee, first_valid_round, last_valid_round, gh, receiver, send_amount,
                                note=note, flat_fee=True)
    signed_tx = tx.sign(Config.algod_private_key)
    tx_id = algod_client.send_transaction(signed_tx)  # wysłanie transakcji
    print(f"Poprawnie zlecono transakcję o ID {tx_id}")
    wait_for_confirmation(algod_client, tx_id=signed_tx.transaction.get_txid())  # oczekiwanie na potwierdzenie
    return cid


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Brak parametru file:
        if 'file' not in request.files:
            flash('Brak parametru file', 'alert alert-danger')
            return redirect(request.url)
        file = request.files['file']
        # Nie wybrano pliku:
        if file.filename == '':
            flash('Nie wybrano pliku!', 'alert alert-warning')
            return redirect(request.url)
        # Wybrano plik o nieprawidłowym rozszerzeniu:
        if not allowed_file(file.filename):
            flash('Wybrano plik o nieprawidłowym rozszerzeniu!', 'alert alert-warning')
            return redirect(request.url)
        # Przesłanie pliku:
        if file:
            files = {'file': (secure_filename(file.filename), file.read(), file.content_type)}
            cid = share_file(files)
            # Flash potwierdzenia przesłania pliku
            flash(f"Plik został przesłany! CID: {cid}", 'alert alert-success')
            return redirect(request.url)
    return render_template('upload_file.html', title='Przesyłanie pliku')


def get_file_content(file_hash):
    url = f"{Config.ipfs_api_address}/api/v0/cat"
    params = (('arg', file_hash),)
    response = requests.post(url, params=params)
    if response.status_code != 200:
        print(response.text)
        raise Exception(f"Invalid status code: '{response.status_code}'.")
    return response.content


def download_file(file_content, file_path):
    file = open(file_path, "wb")
    file.write(file_content)
    file.close()


@app.route('/get_file', methods=['GET', 'POST'])
def get_file():
    if request.method == 'POST':
        # Brak parametru cid:
        if 'cid' not in request.form:
            flash('Brak parametru cid', 'alert alert-danger')
            return redirect(request.url)
        cid = request.form.get('cid')
        # Nie podano cid-a:
        if cid == '':
            flash('Nie podano cid-a!', 'alert alert-warning')
            return redirect(request.url)
        # Pobranie pliku:
        url = f"{Config.ipfs_api_address}/api/v0/ls"
        params = (('arg', cid),)
        response = requests.post(url, params=params)
        if response.status_code != 200:
            flash(response.text, 'alert alert-danger')
            return redirect(request.url)
        result = response.json()
        file = result.get('Objects')[0].get('Links')[0]
        filename = file.get('Name')
        file_hash = file.get('Hash')
        file_content = get_file_content(file_hash)
        download_file(file_content, os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash(f"Plik {filename} został pobrany!", 'alert alert-success')
        return redirect(request.url)
    return render_template('get_file.html', title='Pobieranie pliku')


@app.route('/pastebin', methods=['GET', 'POST'])
def pastebin():
    if request.method == 'POST':
        if 'text' not in request.form:
            flash('Brak parametru text', 'alert alert-danger')
            return redirect(request.url)
        text = request.form.get('text')
        # Nie podano text-u:
        if text == '':
            flash('Nie podano text-u!', 'alert alert-warning')
            return redirect(request.url)
        # Przesłanie text-u:
        if text:
            unique_filename = str(uuid.uuid4()) + '.md'  # utworzenie unikalnej nazwy pliku dla utworzonego text-u
            files = {'file': (unique_filename, text.encode('utf-8'), 'text/plain')}
            cid = share_file(files)
            # Flash potwierdzenia przesłania text-u
            flash(f"Text został przesłany! CID: {cid}", 'alert alert-success')
            return redirect(request.url)
    return render_template('pastebin.html', title='Pastebin')


if __name__ == '__main__':
    app.run(port=Config.flask_port)
