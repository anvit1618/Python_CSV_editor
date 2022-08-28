# PACKAGES
from flask import Flask
from flask import render_template_string
from flask import request
from flask import redirect
import json
import csv
import pandas as pd
from dashh import create_dash_application


# CREATE WEB APP'S INSTANCE
app = Flask('__name__')

create_dash_application(app)

# CREATE NEW CSV ENTRY
@app.route('/create', methods=['GET', 'POST'])
def create():
    #HTTP GET method
    if request.method == 'GET' :

        # get CSV fields from string query parameter
        fields = json.loads(request.args.get('fields').replace("'", '"'))

        #render HTML page dynamically
        return render_template_string('''
                <html>
                    <head>
                        <!-- Bootstrap CDN -->
                        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css">
                    </head>
                    <body>
                        <div class="container mt-5 text-center">
                            <h3>Create New Entry: </h3>
                            <form class="mt-4" method="POST">
                                {% for field in fields %}
                                    <div class="col mt-2">
                                        <div class="row mx-auto" style="width: 350px">
                                            <input name="{{field}}" type="text" class="form-control" placeholder="{{field}}">
                                        </div>  
                                    </div>
                                {% endfor %}

                                <!-- submit form button -->
                                <input type="submit" class="btn btn-success mt-4" value="Submit">
                            </form>
                        </div>
                    </body>
                </html>
        ''', fields=fields)

    #HTTP GET method
    elif request.method == 'POST':
        # extract new CSV entry from submitted form
        data = dict(request.form)

        # udpate the csv file
        with open('price1.csv', 'a') as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            writer.writerow(data)


        # return to READ data page( to see the updates data)
        return redirect('/')    

# READ DATA FROM CSV
@app.route('/')
def read():
    # variable to hold CSV file
    data = []

    #read dta from CSV file
    with open('price1.csv') as f:

        #creat CSV dictionary reader instance
        reader = csv.DictReader(f)

        # loop over CSV rows
        for row in reader:
            data.append(dict(row))

    # render HTML page dynamically
    return render_template_string('''
            <html>
                <head>
                    <!-- Bootstrap CDN -->
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css">
                </head>
                <body>
                    <h1 style="text-align:center;">Equity of Companies</h1>
                    <div class = "container">
                        <!-- CSV data -->
                        <table class="table table-striped mt-5" style="width: 100%; border: 1px solid black">
                            <thead>
                                <tr class="bg-secondary text-white">
                                    {% for header in data[0].keys() %}
                                        <th scope="col">
                                            {% if header == list(data[0].keys())[0] %}
                                                <a class="btn btn-outline-light" href="/create?fields={{str(list(data[0].keys()))}}" style="margin-right: 5px">+</a>
                                            {% endif %}
                                            {{header}}
                                        </th>
                                    {% endfor %}
                                </tr>
                            </thead>
                            <tbody>
                                {% for row in range(0, len(data)) %}
                                    <tr id="{{row}}">
                                        {% for col in range(0, len(list(data[row].values()))) %}
                                            <td style="word-break:breal-all;">
                                                {% if col == 0 %}
                                                    <a class="btn btn-outline-danger" href="/delete?id={{row}}" style="margin-right: 5px">X</a>
                                                    <a href="/update?id={{row}}">{{ list(data[row].values())[col] }}</a>
                                                {% else %}
                                                    {{ list(data[row].values())[col] }}
                                                {% endif %}
                                            </td>
                                        {% endfor %}
                                    </tr>
                                {% endfor %}    
                            </tbody>
                        </table>
                        <a class="btn btn-outline-success" style="width: 100%" href="/dash/" >PLOT</a>
                    </div>
                </body>
            </html>

        ''', data = data, list=list, len=len, str=str)

# update existing CSV row
@app.route('/update', methods=['GET', 'POST'])
def update():
    #HTTP GET method
    if request.method == 'GET' :

        # updated data
        data = []

        #open CSV file
        with open('price1.csv') as rf:
            # create CSV dictionary reader
            reader = csv.DictReader(rf)

            # init CSV rows
            [data.append(dict(row)) for row in reader]

            return render_template_string('''
                <html>
                    <head>
                        <!-- Bootstrap CDN -->
                        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css">
                    </head>
                    <body>
                        <div class="container mt-5 text-center">
                            <h3>Edit the Entry: </h3>
                            <form class="mt-4" method="POST">
                                <div class="col mt-2" hidden>
                                    <div class="row mx-auto" style="width: 350px">
                                        <input name="Id" type="text" class="form-control" value="{{request.args.get('id')}}">
                                    </div>  
                                </div>
                                {% for key, val in fields.items() %}
                                    <div class="col mt-2">
                                        <div class="row mx-auto" style="width: 350px">
                                            <input name="{{key}}" type="text" class="form-control" value="{{val}}">
                                        </div>  
                                    </div>
                                {% endfor %}

                                <!-- submit form button -->
                                <input type="submit" class="btn btn-success mt-4" value="Submit">
                            </form>
                        </div>
                    </body>
                </html>

            ''', fields=data[int(request.args.get('id'))])

    #HTTP POST method
    elif request.method == 'POST' :
        
        # updated data
        data = []

        #open CSV file
        with open('price1.csv') as rf:
            # create CSV dictionary reader
            reader = csv.DictReader(rf)

            # init CSV rows
            [data.append(dict(row)) for row in reader]

        # update row
        row = {}

        for key, val in dict(request.form).items():
            if key != 'Id' :
                row[key] = val

        # update CSV row
        data[int(request.form.get('Id'))] = row

        # write update the CSV file
        with open('price1.csv', 'w') as wf:
            # create CSV dictionary writer
            writer = csv.DictWriter(wf, fieldnames=data[0].keys())
            
            # write CSV column names
            writer.writeheader()
            
            # write CSV rows
            writer.writerows(data)

        # return to READ data page (to see the updated data)
        return redirect('/')

# delete row from CSV file
@app.route('/delete')
def delete():
    # open CSV file
    with open('price1.csv') as rf:
        # updated data
        data = []
        
        # load data
        temp_data = []
        
        # create CSV dictionary reader
        reader = csv.DictReader(rf)
        
        # init CSV rows
        [temp_data.append(dict(row)) for row in reader]
        
        # create mew dataset but without a row to delete
        [
            data.append(temp_data[row]) 
            for row in range(0, len(temp_data))
            if row != int(request.args.get('id'))
        ]

        # update the CSV file
        with open('price1.csv', 'w') as wf:
            # create CSV dictionary writer
            writer = csv.DictWriter(wf, fieldnames=data[0].keys())
            
            # write CSV column names
            writer.writeheader()
            
            # write CSV rows
            writer.writerows(data)

    # return to READ data page (to see the updated data)
    return redirect('/')


# RUN HTTP SERVER
if __name__ == '__main__':
    app.run(debug=True, threaded=True) 