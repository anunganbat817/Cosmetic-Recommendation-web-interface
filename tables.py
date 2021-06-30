from flask_table import Table, Col

class Results(Table):
    id = Col('id', show=False)
    name = Col('name')
    brand = Col('brand')
    price = Col('price')
    list_of_ingredients = Col('list_of_ingredients')
    dist = Col('dist')