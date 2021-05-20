import BotNulis #file BotNulis.py
#impor library yang dibutukan
from flask import Flask,render_template,request,jsonify
from PIL import Image,ImageDraw,ImageFont
import time
import requests
import os

app = Flask(__name__)

waktuFile = time.strftime("%y%m%d-%H%M%S")

@app.route('/')
def index():
  return 'ini index'

@app.route('/write')
def write():
  text = request.args.get('text')
  if not text:
    return jsonify({'error':True,'msg':'Wajib menambahkan argument text '})

  pkertas = request.args.get('kertas')
  if not pkertas:
    pkertas = 1

  pfont = request.args.get('font')
  if not pfont:
    pfont=1

  header = request.args.get('header')
  if not header:
    header =''

  tanggal =request.args.get('tanggal')
  if not tanggal:
    tanggal =''

  bot = BotNulis(text,int(pkertas),int(pfont),header,tanggal)
  result = bot.start()
  return jsonify(result)
