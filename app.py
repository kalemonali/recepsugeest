#!/usr/bin/env python
# coding: utf-8

from flask import Flask, request, jsonify, render_template
import json
from Rp import test

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:

        int_features = [x for x in request.form.values()]
        output = test(int_features[0], int_features[1], int_features[2], int_features[3], int_features[4],
                      int_features[5], [], [])
        result = output.to_json(orient="split")
        parsed = json.loads(result)
        data = json.dumps(parsed)

        b = render_template('index.html', Suggestion_text=data)

        return b
    except:
        return render_template('index.html', Suggestion_text="Wrong Input, Try again")


@app.route('/predict_api', methods=['POST'])
def predict_api():
    if request.method == 'POST':
        try:

            data = json.loads(request.data)

            Food_type = data.get('Food_type')
            Dish_type = data.get('Dish_type')
            veg_non_veg = data.get('veg_non_veg')
            Region = data.get('Region')
            Mood = data.get('Mood')
            Surprise = data.get('Surprise')
            Item = data.get('Item')
            Qty = data.get('Qty')
            #Itemlist = []
            #Qtylist = []


            #for i in range(len(data['Item'])):
                #a = str(data['Item'][i])
                #Itemlist.append(a)
                #b = int(data['Qty'][i])
                #Qtylist.append(b)

            sugges = test(Food_type,Dish_type,veg_non_veg,Region,Mood,Surprise,Item,Qty)
            result1 = sugges.to_json(orient="split")
            result1 = json.loads(result1.replace("\^", " "))
            #parsed = json.loads(result)
            #data = json.dumps(parsed)



        except:
            output = "Wrong Input, Try again"
            result1 = {
                "input error": output
            }

        return jsonify(result1)


if __name__ == "__main__":
    app.run()

