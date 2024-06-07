from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import datetime
from .forms import SearchForm

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Use this utility module to display forms quickly
    Bootstrap5(app)

    # This is a much safer way to store passwords
    Bcrypt(app)

    app.config['SECRET_KEY'] = 'somrandomvalue'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tekkit.sqlite'
    
    db.init_app(app)

    # Config upload folder
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from .models import User, Event
    #from .forms import SearchForm


    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalar(db.select(User).where(User.id == user_id))
    
    from .views import mainbp
    app.register_blueprint(mainbp)

    from . import auth
    app.register_blueprint(auth.authbp)

    from . import events
    app.register_blueprint(events.eventbp)

    @app.errorhandler(404) 
    def not_found(e): 
        return render_template("error.html", error=e)
    
    @app.errorhandler(500) 
    def internal_server_error(e): 
        return render_template("error.html", error=e)

    @app.context_processor
    def get_context():
        year = datetime.datetime.today().year
        return dict(year=year)
    
    return app







    
    

    
    
