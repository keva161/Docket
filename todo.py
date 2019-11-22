from app import app, db
from app.models import User, Todo

if __name__ == '__main__':
    app.run(debug=True)