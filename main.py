from app import app
import os

if __name__ == '__main__':
	app.run(host='127.0.0.1', debug=True, port=os.environ.get('PORT', 5000))
