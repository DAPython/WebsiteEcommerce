from flask import *

app = Flask (__name__)

#Home page
@app.route("/")
def root():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)