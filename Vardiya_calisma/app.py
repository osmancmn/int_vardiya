from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'gelistirme_anahtarı'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vardiya.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    tc_no = db.Column(db.String(11), unique=True, nullable=False)  
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)



class Vardiya(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calisan_ad = db.Column(db.String(100), nullable=False)  # Bu satırı ekle
    baslangic = db.Column(db.DateTime, nullable=False)
    bitis = db.Column(db.DateTime, nullable=False)
    tur = db.Column(db.String(10), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/panel', methods=['GET'])
@login_required
def panel():
    calisanlar = User.query.all()  
    vardiyalar = Vardiya.query.all() 
    return render_template('panel.html', calisanlar=calisanlar, vardiyalar=vardiyalar)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Başarıyla çıkış yaptınız!', category='info')
    return redirect(url_for('index'))


@app.route('/calisan/ekle')
def calisan_ekle():
    return render_template('calisan_ekle.html')


@app.route('/istatistik')
def istatistik():
    return render_template('istatistik.html')


@app.route('/vardiya/ekle', methods=['GET', 'POST'])
@login_required
def gunluk_ekle():
    if request.method == 'POST':
       
        ad = request.form.get('calisan_ad')
        baslangic = request.form.get('baslangic')
        bitis = request.form.get('bitis')
        tur = request.form.get('tur')

      
        baslangic = datetime.strptime(baslangic, '%Y-%m-%dT%H:%M')
        bitis = datetime.strptime(bitis, '%Y-%m-%dT%H:%M')

        yeni_vardiya = Vardiya(calisan_ad=ad, baslangic=baslangic, bitis=bitis, tur=tur)
        db.session.add(yeni_vardiya)
        db.session.commit()

        flash('Vardiya başarıyla kaydedildi!', category='success')
        return redirect(url_for('panel')) 

    return render_template('vardiya_ekle.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        tc_no = request.form.get('tc_no')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Şifreler uyuşmuyor!', category='error')
            return redirect(url_for('register'))

        existing_user = User.query.filter((User.tc_no == tc_no) | (User.email == email)).first()
        if existing_user:
            flash('Bu TC veya e-posta zaten kayıtlı!', category='error')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(Name=name, tc_no=tc_no, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Kayıt başarılı! Giriş yapabilirsiniz.', category='success')
        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        tc_no = request.form.get('tc_no')  
        password = request.form.get('password')

        user = User.query.filter_by(tc_no=tc_no).first()  

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                flash('Giriş başarılı!', category='success')
                return redirect(url_for('panel'))
            else:
                flash('Şifre hatalı!', category='error')
        else:
            flash('T.C. Kimlik Numarası kayıtlı değil!', category='error')

    return render_template('index.html')  



@app.route('/test_db')
def test_db():
    try:
        db.session.query(Vardiya).first()  
        return "Veritabanı bağlantısı başarılı!"
    except Exception as e:
        return f"Veritabanı bağlantısı hatası: {e}"



with app.app_context():
    db.create_all()



import os
if _name_ == "_main_":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
