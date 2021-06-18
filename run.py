from main.app import app
from main.db import db

db.init_app(app)
app.run(debug=True)
