import logging
from flask import Flask, request, redirect, url_for
from flask import render_template, make_response
# from werkzeug.utils import secure_filename


app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        # Перенаправляем на страницу приветсвия,
        # попутно возвращая объект ответа по функцииmake_response
        response = make_response (redirect(url_for('submit')))
        
        # устанавливаем cookie
        response.set_cookie('username', name)
        response.set_cookie('email', email)
        return response
    
    # если запрос GET, то рендерим исходный шаблон
    return render_template('index.html')

# @app.post('/autorization/')
# def autorization():
#     name = request.form['name']
#     email = request.form['email']
#     return redirect(url_for('hello.html', name=name, email=email))

# @app.route('/redirect/')
# def redirect_to_index():
#     return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    logger.warning(e)
    context = {
        'title': 'Страница не найдена',
        'url': request.base_url, 
        }
    return render_template('404.html', **context), 404


@app.route('/hello', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':  # если была нажата кнопка выхода
        # перенаправляем на главную страницу
        response = make_response(redirect(url_for('index')))
        
        # удаляя куки
        response.delete_cookie('username')
        response.delete_cookie('email')
        return response
    
    # если кнопка выхода не была нажата, то есть это перенаправления с главной страницы
    # получаем данные из куки
    username = request.cookies.get('username')
    email = request.cookies.get('email')
    
    # и рендерим страницу с приветствием
    return render_template('hello.html', name=username, email=email)


if __name__ == '__main__':
    app.run(debug=True)