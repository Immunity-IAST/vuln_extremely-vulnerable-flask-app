#!/usr/bin/env python3

from uuid import uuid4

from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask import (Flask, render_template, render_template_string, request,
                   redirect)
from routes import init
from models import RegistrationCode, Session


def setup_db():
    with Session() as session:
        session.execute(f"DELETE FROM {RegistrationCode.__tablename__}")
        for i in range(10):
            code = RegistrationCode()
            code.code = str(uuid4())
            session.add(code)

        session.commit()


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['CKEDITOR_SERVE_LOCAL'] = True
bootstrap = Bootstrap5(app)
login_manager = LoginManager()
login_manager.init_app(app)
ckeditor = CKEditor()

ckeditor.init_app(app)
init()
setup_db()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')


@app.errorhandler(404)
def page_not_found(error):
    detailed_message = render_template_string(
        f"{error}. Requested URL was {request.path}")
    return render_template('404.html', detailed_message=detailed_message)
