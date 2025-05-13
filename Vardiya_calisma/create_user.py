from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    hashed_password = generate_password_hash("1234", method='sha256')
    yeni_kullanici = User(Name="osman", tc_no="10091347656", email="Osmancmn29292@gmail.com", password=hashed_password)
    db.session.add(yeni_kullanici)
    db.session.commit()
    print("Kullanıcı başarıyla eklendi.")
