from app import create_app
import os

if __name__ == '__main__':
	current_app = create_app()
	current_app.run(host='0.0.0.0', port=os.environ.get('PORT', 5005)) #, debug=True)
