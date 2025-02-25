from flask import Flask, render_template_string, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    return render_template_string("""
        <html>
            <head><title>Главная</title></head>
            <body>
                <h1>Добро пожаловать на сайт!</h1>
                <a href="{{ url_for('register') }}">Регистрация</a> | 
                <a href="{{ url_for('login') }}">Вход</a>
            </body>
        </html>
    """)

# Регистрация пользователя
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Проверка на уникальность имени пользователя
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Пользователь с таким именем уже существует', 'danger')
            return redirect(url_for('register'))
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация прошла успешно', 'success')
        return redirect(url_for('login'))
    
    return render_template_string("""
        <html>
            <head><title>Регистрация</title></head>
            <body>
                <h1>Регистрация</h1>
                <form method="POST">
                    <label for="username">Имя пользователя:</label>
                    <input type="text" name="username" required>
                    <br><br>
                    <label for="password">Пароль:</label>
                    <input type="password" name="password" required>
                    <br><br>
                    <button type="submit">Зарегистрироваться</button>
                </form>
                <br>
                <a href="{{ url_for('login') }}">Уже есть аккаунт? Войти</a> | 
                <a href="{{ url_for('index') }}">На главную</a>
            </body>
        </html>
    """)

# Вход в систему
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            flash('Вход успешен', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')
    
    return render_template_string("""
        <html>
            <head><title>Вход</title></head>
            <body>
                <h1>Вход</h1>
                <form method="POST">
                    <label for="username">Имя пользователя:</label>
                    <input type="text" name="username" required>
                    <br><br>
                    <label for="password">Пароль:</label>
                    <input type="password" name="password" required>
                    <br><br>
                    <button type="submit">Войти</button>
                </form>
                <br>
                <a href="{{ url_for('register') }}">Нет аккаунта? Зарегистрироваться</a> | 
                <a href="{{ url_for('index') }}">На главную</a>
            </body>
        </html>
    """)

if __name__ == '__main__':
    db.create_all()  # Создание таблицы в базе данных
    app.run(debug=True)
