from apscheduler.schedulers.background import BackgroundScheduler
from app import create_app, db
from flask_migrate import Migrate
from flask_script import Manager

app = create_app()
app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

from app.routes import *
from app.models import *

def clear_data():
    with app.app_context():
        db.session.query(User).delete()
        db.session.commit()
        print("Deleted User table!")

@manager.command
def run():
    scheduler = BackgroundScheduler()
    scheduler.add_job(clear_data, trigger='interval', hours=1)
    scheduler.start()
    app.run(debug=True)

if __name__ == '__main__':
    manager.run()