from flask import Flask, request, render_template, jsonify
from Service import search_company


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/join', methods=['GET', 'POST'])
def my_form_post():
    url = request.form['domain_url']
    combine = search_company(url)
    result = {
        "output": combine
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)


if __name__ == '__main__':
    app.run(debug=True)
