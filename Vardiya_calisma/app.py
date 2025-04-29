from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calisan/ekle')
def login():
    return render_template('calisan_ekle.html')

@app.route('/istatistik')
def register():
    return render_template('istatistik.html')

@app.route('/panel')
def dashboard():
    return render_template('panel.html')

@app.route('/vardiya/ekle')
def gunluk_ekle():
    return render_template('vardiya_ekle.html')

if __name__ == '__main__':
    app.run(debug=True) 