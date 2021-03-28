from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
                    SubmitField, DecimalField, IntegerField, FileField,\
                    SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo

from app.models import User, Location, Item, etages, buildings


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', \
                 validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_user(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already used. Choose another one.')



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class SearchItem(FlaskForm):
    stringsearch = StringField("Recherche d'un mot-clef: ")
    submit = SubmitField('Chercher!')

class AddItem(FlaskForm):
    name = StringField("Nom: ", validators=[DataRequired()])
    number = IntegerField("Nombre: ", default=1, validators=[DataRequired()])
    location = QuerySelectField(query_factory=lambda: Location.query.all(), validators=[DataRequired()])
    comment = StringField("Commentaire: ")
    photo = FileField("Photo")
    submit = SubmitField('Ajouter!')


class AddLocation(FlaskForm):
    name = StringField("Nom: ", validators=[DataRequired()])
    batiment = SelectField("Batiment: ", choices=[(b,b) for b in buildings])
    etage = SelectField("Étage: ", choices=[(k, i) for k,i in etages.items()])
    piece = StringField("Pièce: ",  validators=[DataRequired()])
    description = StringField("Description: ")
    photo = FileField("Photo")
    submit = SubmitField('Ajouter!')