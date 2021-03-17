import os
from employeeManagement import create_app, db, celery
from employeeManagement.models import User
from flask_migrate import Migrate
import logging


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)


if __name__ == '__main__':
    migrate = Migrate(app, db)
    logging.basicConfig(filename='record.log', level=logging.DEBUG,
                        format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


