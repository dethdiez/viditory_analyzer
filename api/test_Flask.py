from flask import Flask, redirect, url_for, request, render_template
import quickstart
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongo', 27017)
db = client.tododb

item_doc = {'task':'task1', 'description':'description1'}

@app.route("/")
def start():
	#quickstart.get_new_credentials()
	quickstart.main()
	return "Hello World!"
#	_items = db.tododb.find()
#	items = [item for item in _items]
#	return render_template('todo.html', items=items)

@app.route('/new', methods=['POST'])
def new():
	item_doc = {
	'task': request.form['task'],
	'description': request.form['description']
	}
	db.tododb.insert_one(item_doc)
	return redirect(url_for('start'))

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)