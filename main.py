from app import app
import os

if __name__ == '__main__':
	app.run(host='0.0.0.0', port='5005') #os.environ.get('PORT', 5005))
