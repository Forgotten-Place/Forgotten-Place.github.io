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

if __name__ == '__main__':
    app.run(debug=True)
