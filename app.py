from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Album(db.Model):
    __tablename__ = "albums"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    tracks = db.relationship("Track", backref="album", lazy=True)
    
    def __repr__(self):
        return '<Album %r>' % self.id

class Track(db.Model):
    __tablename__ = "tracks"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lyric = db.Column(db.String(800), nullable=False)
    path = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))

    def __repr__(self):
        return '<Track %r>' % self.id

@app.route('/')
def index():
    return render_template('index.html')

#Albums Routes
@app.route('/album', methods=['POST', 'GET'])
def album():
    if request.method == 'POST':
        album_name = request.form['content']
        new_album = Album(name=album_name)

        try:
            db.session.add(new_album)
            db.session.commit()
            return redirect('/album')
        except:
            return 'There was an issue adding your album'

    else:
        albums = Album.query.order_by(Album.date_created).all()
        return render_template('album.html', albums=albums)


@app.route('/album/delete/<int:id>')
def delete_album(id):
    album_to_delete = Album.query.get_or_404(id)

    try:
        db.session.delete(album_to_delete)
        db.session.commit()
        return redirect('/album')
    except:
        return 'There was a problem deleting that album'

@app.route('/album/update/<int:id>', methods=['GET', 'POST'])
def update_album(id):
    album = Album.query.get_or_404(id)

    if request.method == 'POST':
        album.name = request.form['content']

        try:
            db.session.commit()
            return redirect('/album')
        except:
            return 'There was an issue updating your album'

    else:
        return render_template('update_album.html', album=album)

#Track Routes
@app.route('/track', methods=['POST', 'GET'])
def track():
    if request.method == 'POST':
        track_name = request.form['name']
        track_lyric = request.form['lyric']
        track_path = request.form['path']
        album_name = request.form['albums']
        print(album_name)
        track_album = Album.query.filter_by(name=album_name).first()

        new_track = Track(name=track_name, lyric=track_lyric,path=track_path,album= track_album)

        try:
            db.session.add(new_track)
            db.session.commit()
            return redirect('/track')
        except:
            return 'There was an issue adding your track'

    else:
        tracks = Track.query.order_by(Track.date_created).all()
        albums = Album.query.order_by(Album.date_created).all()
        return render_template('track.html', tracks=tracks, albums= albums)

@app.route('/track/delete/<int:id>')
def delete_track(id):
    track_to_delete = Track.query.get_or_404(id)

    try:
        db.session.delete(track_to_delete)
        db.session.commit()
        return redirect('/track')
    except:
        return 'There was a problem deleting that track'

@app.route('/track/update/<int:id>', methods=['GET', 'POST'])
def update_track(id):
    track = Track.query.get_or_404(id)

    if request.method == 'POST':
        track.name = request.form['name']
        track.lyric = request.form['lyric']
        track.path = request.form['path']
        track_album = Album.query.filter_by(name=request.form['albums']).first()
        track.album = track_album
        try:
            db.session.commit()
            return redirect('/track')
        except:
            return 'There was an issue updating your track'

    else:
        albums = Album.query.order_by(Album.date_created).all()
        return render_template('update_track.html', track=track, albums=albums)

if __name__ == "__main__":
    app.run(debug=True)
