from app import app, db
import pandas as pd
import logging 
from db_setup import init_db, db_session
from forms import CosmeticSearchForm
from flask import flash, render_template, request, redirect, jsonify 
from models import SkinCare
from tables import Results
import json, sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sklearn.manifold import TSNE
import numpy as np 
from sqlalchemy.orm import load_only


init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    search = CosmeticSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html', form=search)

@app.route('/results', methods = ['GET', 'POST'])
def search_results(search): 
    results = []
    search_string = search.data['search']
    #qry = db_session.query(SkinCare).filter(SkinCare.brand == search_string)
    
    qry = db.session.query(SkinCare).filter(func.lower(SkinCare.name).op('regexp')(r'\b{}\b'.format(search_string)))
    results = qry.first()
    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        xx = results.category
        # display results
        #moisturizer = db.session.query(SkinCare).options(load_only(*fields)).filter(func.lower(SkinCare.category).op('regexp')(r'\b{}\b'.format(xx)))
        moisturizer = SkinCare.query.with_entities(SkinCare.name, SkinCare.brand, SkinCare.price, SkinCare.category, SkinCare.list_of_ingredients).filter(SkinCare.category == xx)
        moisturizer = moisturizer.all()
        moisturizer = pd.DataFrame(moisturizer, columns=['name', 'brand','price', 'category', 'list_of_ingredients'])

        ingredient_lists = {}
        data = []
        lists = 0 
        for i in range(len(moisturizer)):    
            ingredients = moisturizer['list_of_ingredients'][i]
            ingredients_lower = ingredients.lower()
            tokens = ingredients_lower.split(', ')
            data.append(tokens)
            for ingredient in tokens:
                if ingredient not in ingredient_lists:
                    ingredient_lists[ingredient] = lists
                    lists += 1

        M = len(moisturizer)  # The number of the items
        N = len(ingredient_lists)    
        A = np.zeros((M, N))    

        def oh_encoder(tokens):
            x = np.zeros(N)    
            for ingredient in tokens:
                # Get the index for each ingredient
                idx = ingredient_lists[ingredient]
                # Put 1 at the corresponding indices
                x[idx] = 1
            return x

        i = 0
        for tokens in data:
            A[i, :] = oh_encoder(tokens)
            i += 1

        model = TSNE(n_components = 2, learning_rate = 250)
        tsne_features = model.fit_transform(A)  
        moisturizer['X'] = tsne_features[:, 0]
        moisturizer['Y'] = tsne_features[:, 1]
        moisturizer['dist'] = 0.0
        myProduct = moisturizer[moisturizer.name.str.contains(results.name)]
        p1 = np.array([myProduct.X.values, myProduct.Y.values]).reshape(1, -1)

        for i in range(len(moisturizer)):
            p2 = np.array([moisturizer['X'][i], moisturizer['Y'][i]]).reshape(-1, 1)
            moisturizer.dist[i] = ((p1 * p2).sum() / (np.sqrt(np.sum(p1))*np.sqrt(np.sum(p2))))

        table = moisturizer.sort_values('dist').head(5)
        table = table[['name','brand','price','category','dist']]
        #table = Results(moisturizer)
        #table.border = True
        #return render_template('results.html', table=table)
        print(table)
    return render_template('simple.html',  tables=[table.to_html(classes='center')], titles=table.columns.values)
#@app.route("/")
#def index():
    #return render_template('index.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)