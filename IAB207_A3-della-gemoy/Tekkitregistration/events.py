from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, Booking
from .forms import  EventForm, SearchForm
from . import db
import os
from werkzeug.utils import secure_filename
# additional import:
from flask_login import login_required, current_user
from sqlalchemy import or_


eventbp = Blueprint('event', __name__, url_prefix='/events')

@eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
    event_form = EventForm()
    if event_form.validate_on_submit():
        db_file_path = check_upload_file(event_form)
        event = Event(name=event_form.name.data,description=event_form.description.data, 
        image=db_file_path,currency=event_form.currency.data)
        db.session.add(event)
        db.session.commit()
        flash('New event created successfully! :D', 'success')
        return redirect(url_for('event.create_event'))
    return render_template('create_event.html', form=event_form)
    
@eventbp.route('/booking-history')
@login_required
def booking_history():
    booking = db.session.scalar(db.select(Booking).where(Booking.id==id))
    if not booking:
       abort(404)
    return render_template('booking_history.html', booking=booking)

def check_upload_file(form):
  fp = form.image.data
  filename = fp.filename
  BASE_PATH = os.path.dirname(__file__)
  upload_path = os.path.join(BASE_PATH, '/static/image', secure_filename(filename))
  db_upload_path = '/static/image/' + secure_filename(filename)
  fp.save(upload_path)
  return db_upload_path

@eventbp.route('/search', methods=["GET", "POST"])
def search():
    search_form = SearchForm()
    posts = []
    post_searched = ""
    selected_genre = ""
    
    if request.method == "POST" and search_form.validate_on_submit():
        post_searched = search_form.searched.data.strip()
        selected_genre = search_form.genre.data
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
    
    return render_template("index.html", form=search_form, searched=post_searched, genre=selected_genre, posts=posts)


@eventbp.route('/<id>')
def event_details(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if not event:
       abort(404)
    return render_template('event_details.html', event=event)