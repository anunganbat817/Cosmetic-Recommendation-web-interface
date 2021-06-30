
from wtforms import Form, StringField, SelectField

class CosmeticSearchForm(Form):
    choices = [('name', 'name'),
               ('brand', 'brand'),
               ('category', 'category')]
    select = SelectField('Search for product:', choices=choices)
    search = StringField('')