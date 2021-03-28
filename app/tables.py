from app.models import User, Location, Item
from flask_table import Table, Col, LinkCol
from flask import url_for


classes = ['table', 'table-striped', 'table-bordered', 'table-condensed']
class ResultTable(Table):
    classes = classes
    name = LinkCol('Name', 'items', url_kwargs=dict(identifier='id'), attr='name')
    location = LinkCol('Location', 'locations', url_kwargs=dict(identifier='location.id'), attr='location.nom')


class LocationTable(Table):
    classes = classes
    nom = LinkCol('nom', 'locations', url_kwargs=dict(identifier='id'), attr='nom')
    batiment = Col("batiment")
    etage = Col("etage")
    piece = Col("piece")

