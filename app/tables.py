from app.models import User, Location, Item
from flask_table import Table, Col, LinkCol
from flask import url_for


classes = ['table', 'table-striped', 'table-bordered', 'table-condensed']
class ResultTable(Table):
    classes = classes
    Nom = LinkCol('Nom', 'items', url_kwargs=dict(identifier='id'), attr='name')
    Rangement = LinkCol('Rangement', 'locations', url_kwargs=dict(identifier='location.id'), attr='location.nom')


class LocationTable(Table):
    classes = classes
    Nom = LinkCol('Nom', 'locations', url_kwargs=dict(identifier='id'), attr='nom')
    batiment = Col("Bâtiment")
    etage = Col("Étage")
    piece = Col("Pièce") 