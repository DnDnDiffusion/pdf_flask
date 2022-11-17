import math
import os
# Importing the statistics module
import statistics
from os.path import dirname, join, realpath
from time import time
import matplotlib.pyplot as plt
import numpy as np
import PyPDF2
from flask import (Flask, Response, flash, redirect, render_template, request,
                   url_for)
from flask import Flask, render_template, request, url_for, jsonify
#make a POST request
import requests
from flask import request
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from flask import Flask, redirect, url_for, request



app=Flask(__name__,template_folder='templates')
# importing required modules


# Upload folder
# UPLOAD_FOLDER = 'static/files'
# app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
app.config["UPLOAD_FOLDER"] = "static/"

# creating a pdf file object

quarks = [{'name': 'up', 'charge': '+2/3'},
          {'name': 'down', 'charge': '-1/3'},
          {'name': 'charm', 'charge': '+2/3'},
          {'name': 'strange', 'charge': '-1/3'}]

@app.route('/hello_world', methods=['GET'])
def hello_world():
    return jsonify({'message' : 'Hello, World!'})

@app.route('/quarks', methods=['GET'])
def returnAll():
    return jsonify({'quarks' : quarks})

@app.route('/quarks/<string:name>', methods=['GET'])
def returnOne(name):
    theOne = quarks[0]
    for i,q in enumerate(quarks):
      if q['name'] == name:
        theOne = quarks[i]
    return jsonify({'quarks' : theOne})

@app.route('/quarks', methods=['POST'])
def addOne():
    new_quark = request.get_json()
    quarks.append(new_quark)
    return jsonify({'quarks' : quarks})

@app.route('/quarks/<string:name>', methods=['PUT'])
def editOne(name):
    new_quark = request.get_json()
    for i,q in enumerate(quarks):
      if q['name'] == name:
        quarks[i] = new_quark    
    qs = request.get_json()
    return jsonify({'quarks' : quarks})

@app.route('/quarks/<string:name>', methods=['DELETE'])
def deleteOne(name):
    for i,q in enumerate(quarks):
      if q['name'] == name:
        del quarks[i]  
    return jsonify({'quarks' : quarks})











@app.route('/')
def upload_file():
    return render_template('index.html')


@app.route('/display', methods = ['GET', 'POST'])
def save_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)

        f.save(app.config['UPLOAD_FOLDER'] + filename)

        # file = open(,"r")
        pdfFileObj = open(app.config['UPLOAD_FOLDER'] + filename, 'rb')
	
        # creating a pdf reader object
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

        # printing number of pages in pdf file
        print(pdfReader.numPages)

        # creating a page object
        pageObj1 = pdfReader.getPage(0)
        pageObj2 = pdfReader.getPage(1)

        # extracting text from page
        text = pageObj1.extractText() + "\n" + pageObj2.extractText()


        # closing the pdf file object
        pdfFileObj.close()
        word = text
        
        indexSRace=word.find('RACE/ANCESTRY/HERITAGE') + 22
        indexERace= word.find('BACKGROUND') 
        character_race = word[indexSRace:indexERace]

        indexSClassLevel=word.find('CLASS & LEVEL') + 13
        indexEClassLevel=word.find('EXPERIENCE') - 2
        character_classLevel = word[indexSClassLevel:indexEClassLevel]
          #weapon -> action -> cleric-healing, artificer has interesting weapons
          
        prompt = "character portrait for Level " + word[indexEClassLevel] + " " + character_race + character_classLevel + ", greg rutkowski, Fujiwara Nobuzane, Cao Zhibai, artstation"
        return render_template('content.html', content=prompt) 




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug = True)
