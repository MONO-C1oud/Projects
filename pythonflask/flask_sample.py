import flask
from flask import *

app = Flask(__name__)


@app.route("/", methods=['POST','GET'])
def index():
	return render_template('index.html')

	
@app.route("/results",methods=['GET','POST'])
def results():
	name = request.form.get('username')
	return render_template("index.html",name=name)

if __name__ == '__main__':
	app.run(debug=True,port=1337)