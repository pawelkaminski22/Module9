from flask import Flask, request, redirect, render_template
import requests
import csv

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def message():
    if request.method == 'GET':
        return render_template("form.html", currency=currency)
    elif request.method == 'POST':
        data = request.form
        curr_value = data.get('curr_value')
        selected_curr = data.get('curr')

        for i in currency:
            if i['currency'] == selected_curr:
                curr_to_count = i['ask']

        pln_value = float(curr_value) * float(curr_to_count)
        return f'Otrzymasz kwotę: {pln_value:.2f} PLN'


def get_currency(url):
    response = requests.get(url)
    data = response.json()
    return data


def write_currency_csv(path, currency):
    header = ['currency', 'code', 'bid', 'ask']
    with open(path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header, delimiter=';')
        writer.writeheader()
        writer.writerows(currency)
    print('Table saved')


if __name__ == "__main__":
    table = get_currency("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    currency = table[0]['rates']

    file_name = 'C:\\Kodilla\\Module_9\\curr.csv'
    write_currency_csv(file_name, currency)

    print(table)
    print(table[0]['rates'])

    app.run(debug=True)

