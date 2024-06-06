from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import datetime
from sqlalchemy import or_

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
    
    @app.route('/search', methods=["GET", "POST"])
    def search():
        form = SearchForm()
        posts = []
        post_searched = ""
        selected_genre = ""
        
        if request.method == "POST" and form.validate_on_submit():
            post_searched = form.searched.data.strip()
            selected_genre = form.genre.data
            print(f"Searching for exact match: {post_searched}, Genre: {selected_genre}")  # Debugging
            
            # Query for exact matches with optional genre filtering
            query = Event.query.filter(
                or_(
                    Event.name == post_searched,
                    Event.artist == post_searched
                )
            )
            
            if selected_genre:
                query = query.filter(Event.genre == selected_genre)
            
            posts = query.order_by(Event.startDateTime).all()
            print(f"Found posts: {posts}")  # Debugging
        
        return render_template("index.html", form=form, searched=post_searched, genre=selected_genre, posts=posts)

    from .models import User, Event
    from .forms import SearchForm
    
    # Context processor for navbar
    @app.context_processor
    def base():
        form = SearchForm()
        return dict(form=form)

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