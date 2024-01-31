from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from Sem_3_forms import *


app = Flask(__name__)
app.config['SECRET_KEY'] = b'2bc64352bdsrt2357h456g'
csrf = CSRFProtect(app)


@app.route('/')
def index():
    return 'HI'


@app.route('/data/')
def data():
    return 'Your data'


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        pass
    return render_template('login.html', form=form)



@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
# Обработка данных из формы
        email = form.email.data
        password = form.password.data
        print(email, password)
        ...
    return render_template('register.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/form', methods=['GET', 'POST'])
# @csrf.exempt
# def my_form():
#     return 'NO CSRF protection'