from apscheduler.schedulers.background import BackgroundScheduler
from app import create_app, db
from app.models import Todo, User
from flask_script import Manager

app = create_app()

manager = Manager(app)

def clear_data():
    with app.app_context():
        db.session.query(User).delete()
        db.session.query(Todo).delete()
        db.session.commit()
        print("Deleted table rows!")

@manager.command
def run():
    scheduler = BackgroundScheduler()
    scheduler.add_job(clear_data, trigger='interval', minutes=15)
    scheduler.start()
    app.run(debug=True)

if __name__ == '__main__':
    clear_data()
    manager.run()