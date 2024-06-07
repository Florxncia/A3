from flask import Blueprint, render_template, request
from .models import Event
from . import db


mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()    
    return render_template('index.html', events=events)

