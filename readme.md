#Install enviroment

python3 -m virtualenv venv
ls
mkdir project
ls
source venv/bin/activate
python --version
pip install flask

export FLASK_ENV=development
export FLASK_APP=app

flask run

Create database:
from project.database import db
db.create_all()
db