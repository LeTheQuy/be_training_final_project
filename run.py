from main.app import app
from main.db import db

db.init_app(app)
app.run(debug=True)


@app.before_first_request
def create_tables():
    db.create_all()
