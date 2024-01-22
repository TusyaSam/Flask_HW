from flask import Flask, render_template, request, redirect, url_for
from models import db, Human
from flask_wtf.csrf import CSRFProtect
import secrets
from Sem_3_forms import RegisterForm
from sqlalchemy import inspect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../instance/mydatabase.db'
db.init_app(app)
app_secret = secrets.token_hex()
app.secret_key = app_secret
csrf = CSRFProtect(app)

@app.route('/')
def index():
    human = Human.query.all()
    return render_template('index.html', human=human)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        password = form.password.data
        print(name, surname, email, password)
        human = Human(name=form.name.data, 
                      surname=form.password.data, 
                      email=form.email.data, 
                      password=form.password.data.encode(encoding='UTF-8'))
        db.session.add(human)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.route('/human/')
def human():
    human = Human.query.all()
    context = {'human': human}
    return render_template('human.html', **context)


def all_tables_exist() -> bool:
    
    wanted_tables = db.metadata.tables
    db_inspector = inspect(db.engine)
    existed_tables_list = db_inspector.get_table_names()
    for table_name, table_data in wanted_tables.items():
        if table_name not in existed_tables_list:
            return False
        existed_table_columns = {el['name']: el for el in inspect(db.engine).get_columns('human')}
        for column_name, wanted_column_data in table_data.columns.items():
            if column_name not in existed_table_columns:
                raise Exception("Incorrect SQL structure, check database scheme")
            existed_column_info = dict()
            wanted_column_info = dict()
            for column_param in existed_table_columns[column_name]:
                if column_param == 'primary_key':
                    existed_column_info[column_param] = bool(existed_table_columns[column_name][column_param])
                    wanted_column_info[column_param] = wanted_tables[table_name].columns[
                        column_name].__getattribute__(column_param)
                elif column_param == 'type':
                    col_param = existed_table_columns[column_name][column_param]
                    col_len = ""
                    if "length" in existed_table_columns[column_name][column_param].__dict__:
                        col_len = str(col_param.length)
                    existed_column_info[column_param] = col_param.python_type.__name__ + col_len
                    col_param = wanted_tables[table_name].columns[column_name].__getattribute__(column_param)
                    col_len = ""
                    if "length" in wanted_tables[table_name].columns[column_name].type.__dict__:
                        col_len = str(col_param.length)
                    wanted_column_info[column_param] = col_param.python_type.__name__ + col_len
                else:
                    existed_column_info[column_param] = existed_table_columns[column_name][column_param]
                    wanted_column_info[column_param] = wanted_tables[table_name].columns[
                        column_name].__getattribute__(column_param)
            for column_param in existed_column_info:
                if column_param != 'type' and existed_column_info[column_param] != wanted_column_info[column_param]:
                    raise Exception("Incorrect SQL structure, check database scheme")
    return True


if __name__ == '__main__':
    app.run(debug=True)