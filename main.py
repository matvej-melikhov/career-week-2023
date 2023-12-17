# -*- coding: utf-8 -*

from app import application
from app import migrate

from app.routes import *
from app.models import *

from app import admin
from flask_admin.contrib.sqla import ModelView

from app import db

from flask import Response, request
from werkzeug.exceptions import HTTPException

class UserView(ModelView):
    page_size = 100
    can_export = True
    column_display_pk = True
    column_searchable_list = ['name', 'email']
    column_filters = ['name', 'email']
    form_columns = ["id", "name", "course", "grade", "email", "reason"]

admin.add_view(UserView(User, db.session))

# Protect admin panel using Basic Auth
@application.before_request
def restrict_admin():
    if request.path.startswith("/admin/info"):
        auth = request.authorization
        if not auth or not (auth.username == application.config.get("ADMIN_USERNAME", "admin") and 
                            auth.password == application.config.get("ADMIN_PASSWORD", "sokt2023")):
            raise HTTPException('', Response(
                "Could not verify your access level for that URL.\n"
                "You have to login with proper credentials", 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            ))

# Ensure database tables are created automatically
with application.app_context():
    db.create_all()

if __name__ == "__main__":
    application.run(host="0.0.0.0", debug=True)