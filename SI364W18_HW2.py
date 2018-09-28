## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist 
## and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

## Ava Weiner helped me debug /specific/song/<artist_name> route.
## Kevin Rothstein helped me with album_data.html, explained <p> to me. 
## Used https://stackoverflow.com/questions/14591202/how-to-make-a-radiofield-in-flask & https://stackoverflow.com/questions/47627042/how-do-i-add-a-class-to-wtform-radio-field to help with AlbumEntryForm class.

#############################
##### IMPORT STATEMENTS #####
#############################


from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required


import requests
import json


#####################
##### APP SETUP #####
#####################


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'
app.debug = True

####################
###### FORMS #######
####################


class AlbumEntryForm(FlaskForm):
	name_album = StringField('Enter the name of an album:', validators = [Required()])
	radio_buttons = RadioField('How much do you like this album? (1 low, 3 high)', choices = [('1','1'), ('2','2'), ('3','3')], validators = [Required()])
	submit = SubmitField('Submit')


####################
###### ROUTES ######
####################


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)


@app.route('/artistform')
def artist_form():
	return render_template('artistform.html')


@app.route('/artistinfo', methods = ['GET', 'POST'])
def artist_info():
	artist = request.args.get('artist')
	params = {}
	params['term'] = artist
	params['entity'] = 'musicTrack'
	response = requests.get('https://itunes.apple.com/search',  params = params)
	my_response = json.loads(response.text)['results']
	my_tracks = []
	for track in my_response:
		my_tracks.append(track)
	return render_template('artist_info.html', objects = my_tracks)


@app.route('/artistlinks')
def artistlinks():
	return render_template('artist_links.html')


@app.route('/specific/song/<artist_name>', methods = ['GET', 'POST'])
def specific_artist(artist_name):
	new_params = {}
	new_params['term'] = artist_name
	new_params['song'] = 'musticTrack'
	another_response = requests.get('https://itunes.apple.com/search', params = new_params)
	json_response = json.loads(another_response.text)['results']
	return render_template('specific_artist.html', results = json_response)


@app.route('/album_entry')
def album_entry():
	my_form= AlbumEntryForm()
	return render_template('album_entry.html', form = my_form)

@app.route('/album_result', methods = ['GET', 'POST'])
def album_result():
	form = AlbumEntryForm(request.form)
	if request.method == 'POST' and form.validate_on_submit():
		name_album = form.name_album.data
		radio_buttons = form.radio_buttons.data
		return render_template('album_data.html', name_album = name_album, radio_buttons = radio_buttons)

	flash('All fields are required!')
	return redirect(url_for('album_entry'))


if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
