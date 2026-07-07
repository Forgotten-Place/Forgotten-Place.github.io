from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html', active_page='index')

@app.route('/predystoriya')
def predystoriya():
    return render_template('predystoriya.html', active_page='predystoriya')

@app.route('/lor-chernovodska')
def lor_chernovodska():
    return render_template('lor_chernovodska.html', active_page='lor_chernovodska')

@app.route('/obshestvo-rassveta')
def obshestvo_rassveta():
    return render_template('obshestvo_rassveta.html', active_page='obshestvo_rassveta')

@app.route('/dizdok-zbt')
def dizdok_zbt():
    return render_template('dizdok_zbt.html', active_page='dizdok_zbt')

if __name__ == '__main__':
    app.run(debug=True)
