import json
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    result = db.relationship('Result', backref='user', lazy=True)


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def home():
    return redirect(url_for('quiz'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Kayıt başarılı! Giriş yapabilirsiniz.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('quiz'))
        else:
            flash('Geçersiz kullanıcı adı veya şifre', 'danger')
    return render_template('login.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()


def load_questions():
    with open('./questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['questions']

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    questions = load_questions()

    if request.method == 'POST':
        score = 0
        for question in questions:
            user_answer = request.form.get(question['id'])
            if question['type'] == 'text':
                if user_answer.lower().strip() == question['answer'].lower().strip():
                    score += 1
            else:
                if user_answer == question['answer']:
                    score += 1

        user_result = Result.query.filter_by(user_id=current_user.id).first()
        if user_result:
            if score > user_result.score:
                user_result.score = score
                db.session.commit()
        else:
            new_result = Result(score=score, user_id=current_user.id)
            db.session.add(new_result)
            db.session.commit()

        return render_template('quiz_result.html', score=score)

    return render_template('quiz.html', questions=questions, best_score=current_user.result[0].score if current_user.result else 0)



if __name__ == '__main__':
    app.run(debug=True)
