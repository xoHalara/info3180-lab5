"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""
from flask import render_template, request, jsonify, send_file, Blueprint, send_from_directory
from flask import current_app as app
from app.forms import MovieForm
from app.models import Movie
from app import db, csrf
from werkzeug.utils import secure_filename
import os
from datetime import datetime

main = Blueprint('main', __name__)

###
# Routing for your application.
###

@main.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@csrf.exempt
@main.route('/api/v1/movies', methods=['GET', 'POST'])
def movies():
    if request.method == 'POST':
        form = MovieForm()
        if form.validate_on_submit():
            title = form.title.data
            description = form.description.data
            poster = form.poster.data
            
            # Save the poster file
            filename = secure_filename(poster.filename)
            poster.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Create new movie record
            movie = Movie(title=title, description=description, poster=filename)
            db.session.add(movie)
            db.session.commit()
            
            return jsonify({
                "message": "Movie successfully added",
                "title": title,
                "description": description,
                "poster": filename
            })
        return jsonify({"errors": form.errors}), 400
    
    # GET request - return all movies
    try:
        movies = Movie.query.all()
        return jsonify({
            "movies": [{
                "id": movie.id,
                "title": movie.title,
                "description": movie.description,
                "poster": f"/api/v1/posters/{movie.poster}"
            } for movie in movies]
        })
    except Exception as e:
        app.logger.error(f"Error in GET /api/v1/movies: {str(e)}")
        return jsonify({"error": str(e)}), 500

@main.route('/api/v1/posters/<filename>')
def get_poster(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@main.route('/api/v1/movies/<int:movie_id>', methods=['DELETE'])
@csrf.exempt
def delete_movie(movie_id):
    try:
        movie = Movie.query.get_or_404(movie_id)
        
        # Delete the poster file
        poster_path = os.path.join(app.config['UPLOAD_FOLDER'], movie.poster)
        if os.path.exists(poster_path):
            os.remove(poster_path)
        
        # Delete from database
        db.session.delete(movie)
        db.session.commit()
        
        return jsonify({
            "message": "Movie successfully deleted",
            "id": movie_id
        })
    except Exception as e:
        app.logger.error(f"Error deleting movie: {str(e)}")
        return jsonify({"error": str(e)}), 500

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@main.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@main.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@main.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404