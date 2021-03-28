from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user,\
                        login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from sqlalchemy import or_


from os.path import join
from datetime import datetime


from app import app, db, Config
from app.forms import LoginForm, RegistrationForm, SearchItem, AddItem, AddLocation, DeleteForm
from app.models import User, Location, Item
from app.tables import ResultTable, LocationTable


@app.route('/')
@app.route('/index')
def index():
  if current_user.is_authenticated:
    ncurrent = db.session.query(Item).filter(Item.item_creator==current_user).count()
  else:
    ncurrent = -1
  return render_template('index.html', title='organisateur', ncurrent=ncurrent)


@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data.lower()).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      return redirect(url_for('index'))
    return redirect(next_page)
  return render_template('login.html', title="Sign in", form=form)

@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Merci {user.username}, tu es maintenant un rangeur.")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/add_object', methods=['GET', 'POST'])  
@login_required
def add_object():
    form = AddItem()
    if form.validate_on_submit():
      name = form.name.data 
      number = form.number.data
      location = form.location.data 
      comment = form.comment.data 
      # build filename for pic:      
      if form.photo.data:
        timestamp = datetime.strftime(datetime.now(), "%Y_%m_%d_%H_%M_%S")
        filename = secure_filename(f"{name}_{timestamp}.jpg")
        filename = join(Config.ITEMS_PICTURES, filename)
        # save pic:
        form.photo.data.save(filename)
      else:
        filename = ''

      # add to database:
      now = datetime.now()
      new = Item(name=name,
                comment=comment,
                number=number,
                item_location=location,
                item_creator=current_user,
                photopath=filename,
                created=now,
                lastmodified=datetime.now())
      db.session.add(new)
      db.session.commit()
      flash("Nouvel objet ajouté !")
      new = db.session.query(Item).filter(Item.name==name).filter(Item.created==now).first()
      return redirect(f'/items/{new.id}')

    return render_template('add_object.html', form=form)


@app.route('/add_location', methods=['GET', 'POST'])  
@login_required
def add_location():
    form = AddLocation()
    if form.validate_on_submit():
      name = form.name.data 
      batiment = form.batiment.data 
      etage = form.etage.data 
      piece = form.piece.data 
      description = form.description.data 
      # build filename for pic:
      if form.photo.data:
        timestamp = datetime.strftime(datetime.now(), "%Y_%m_%d_%H_%M_%S")
        filename = secure_filename(f"{name}_{timestamp}.jpg")
        filename = join(Config.LOCATIONS_PICTURES, filename)
        # save pic:
        form.photo.data.save(filename)
      else:
        filename = ''
      # add to database:
      new = Location(nom=name,
                    batiment=batiment,
                    description=description,
                    etage=etage,
                    piece=piece,
                    location_creator=current_user,
                    photopath=filename)
      db.session.add(new)
      db.session.commit()
      flash("Nouveau rangement ajouté !")
    return render_template('add_location.html', form=form)




@app.route('/search', methods=['GET', 'POST'])  
def search():
    form = SearchItem()
    objects = []
    if form.validate_on_submit():
        stringsearch = form.stringsearch.data
        objects = db.session.query(Item).filter(or_(Item.name.contains(stringsearch),Item.comment.contains(stringsearch)))
    table = ResultTable(objects)

    return render_template('search.html', form=form, table=table)


@app.route('/items/<identifier>')
def items(identifier):
  item = db.session.query(Item).filter(Item.id==int(identifier)).first()
  path = item.photopath   
  path = path.replace('app/static/', '')
  return render_template('item.html', item=item, path=path, form=False)


@app.route('/items/modify/<identifier>', methods=['GET', 'POST'])  
@login_required
def modifyItem(identifier):
  item = db.session.query(Item).filter(Item.id==int(identifier)).first()
  path = item.photopath 
  path = path.replace('app/static/', '')
  form = AddItem(location=item.location, number=item.number, name=item.name, comment=item.comment)
  if form.validate_on_submit():
    if form.name.data:
      item.name = form.name.data 
    if form.number.data:
      item.number = form.number.data 
    if form.location.data:
      item.location = form.location.data 
    if form.comment.data:
      item.comment = form.comment.data 
    # build filename for pic:      
    if form.photo.data:
      timestamp = datetime.strftime(datetime.now(), "%Y_%m_%d_%H_%M_%S")
      filename = secure_filename(f"{name}_{timestamp}.jpg")
      filename = join(Config.ITEMS_PICTURES, filename)
      # save pic:
      form.photo.data.save(filename)
      item.photopath = filename
    else:
      filename = ''
    # add to database:
    item.lastmodified = datetime.now()
    db.session.add(item)
    db.session.commit()
    flash(f"Objet {item.name} modifié !")  
    return redirect(f'/items/{item.id}')
  else:
    for fieldName, errorMessages in form.errors.items():
      for err in errorMessages:
        flash(err)
  return render_template('item.html', item=item, path=path, form=form)

@app.route('/items/delete/<identifier>', methods=['GET', 'POST'])  
@login_required
def deleteItem(identifier):
  item = db.session.query(Item).filter(Item.id==int(identifier)).first()
  form = DeleteForm()
  if form.validate_on_submit():
    if form.really.data:
      db.session.delete(item)
      db.session.commit()
      flash(f"{item.name} supprimé!")
      return redirect('/index')
    else:
      flash(f"{item.name} préservé")
      return redirect(f'/items/{item.id}')
  return render_template('delete.html', form=form)


@app.route('/locations/<identifier>')
def locations(identifier):
  location = db.session.query(Location).filter(Location.id==int(identifier)).first()
  path = location.photopath 
  path = path.replace('app/static/', '')
  # check items stored there:
  objects = db.session.query(Item).filter(Item.location == location)
  table = ResultTable(objects)
  return render_template('location.html', location=location, path=path, table=table)

@app.route('/list_locations')
def list_locations():
  locations = db.session.query(Location)
  table = LocationTable(locations)
  return render_template('list_locations.html', table=table)


@app.route('/404')
def notfound():
  return render_template('404.html')
