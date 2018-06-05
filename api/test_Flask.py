from flask import Flask, redirect, url_for, request, render_template
import quickstart
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongo', 27017)
db = client.tododb

item_doc = {'task':'task1', 'description':'description1'}

@app.route("/auth")
def auth():
	credentials = quickstart.get_new_credentials()
	return credentials

@app.route("/analyze")
def analyze():
	quickstart.test()
	return("Success")

@app.route('/new', methods=['POST'])
def new():
	task = request.args.get("task", type = str),
	description = request.args.get("description")
	#db.tododb.insert_one(item_doc)
	return (task[0])

@app.route('/test', methods=['POST'])
def test():
	return ("Success")

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)