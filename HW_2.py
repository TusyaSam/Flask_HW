import logging
from flask import Flask, request, redirect, url_for
from flask import render_template, make_response
from werkzeug.utils import secure_filename


app = Flask(__name__)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    # # устанавливаем cookie
    # response = make_response("Cookie установлен")
    # response.set_cookie('username', 'admin')
    # return response
    return render_template('autorization.html')

# @app.post('/autorization/')
# def autorization():
#     name = request.form['name']
#     email = request.form['email']
#     return redirect(url_for('hello.html', name=name, email=email))

@app.route('/redirect/')
def redirect_to_index():
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    logger.warning(e)
    context = {
        'title': 'Страница не найдена',
        'url': request.base_url, 
        }
    return render_template('404.html', **context), 404


@app.route('/hello', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    return render_template('hello.html', name=name, email=email)



# @app.route('/getcookie/')
# def get_cookies():
#     # получаем значение cookie
#     name = request.cookies.get('username')
#     return f"Значение cookie: {name}"


if __name__ == '__main__':
    app.run(debug=True)