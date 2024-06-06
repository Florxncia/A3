from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, Comment
#from .forms import  EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
# additional import:
from flask_login import login_required, current_user

eventbp = Blueprint('event', __name__, url_prefix='/events')