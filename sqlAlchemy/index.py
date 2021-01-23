from flask import Flask, request, flash, url_for, redirect, send_file, render_template
import numpy as np
import os
from matplotlib import pyplot as plt 
from matplotlib.image import imread, imsave
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session

host = '127.0.0.1'
port = 3306
db = 'depth'
user = 'root'
password = 'zsy007'

img_path = './static/img/'
cmps = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn',
 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 
 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r',
  'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 
  'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 
  'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 
  'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 
  'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 
  'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 
  'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 
  'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 
  'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool',
   'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r',
    'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r','gist_heat', 'gist_heat_r', 'gist_ncar', 
    'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 
    'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 
    'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'viridis', 'viridis_r', 'winter', 'winter_r']

engine = create_engine(str(r"mysql+mysqldb://%s:" + '%s' + "@%s/%s?charset=utf8") % (user, password, host, db))
Session = scoped_session(sessionmaker(bind=engine))
session = Session()


app = Flask(__name__)

if not os.path.exists(img_path):
  os.makedirs(img_path)

@app.route('/')
def hello_world():
    return render_template('index.html', len = len(cmps), cmps = cmps)

@app.route('/img_frame', methods=['POST'])
def queryImg():
  depth_min = request.form['depth_min']
  depth_max = request.form['depth_max']
  cmp = request.form['cmp']
  print(depth_min, depth_max, cmp, type(depth_min))
  filename = str(depth_min)+'_'+str(depth_max)+'_'+cmp
  filename = filename.replace('.', '-') + '.png'
  filepath = img_path + filename
  
  if os.path.exists(filepath):
    print(filepath + ' exists')
    return send_file(filepath, mimetype='image/png')
  select_sql =r'SELECT * FROM layer WHERE depth > %f AND depth < %f ' % (float(depth_min), float(depth_max))
      
  print(filepath + ' not exists')
  print(text(select_sql))
  result = session.execute(text(select_sql))

  res = []
  for row in result:
      res.append(row)
  res_img = np.asarray(res)[:, 1:]
  print(res_img.shape)

  imsave(filepath, res_img, cmap=cmp)
  return send_file(filepath, mimetype='image/png')



if __name__ == '__main__':
    app.run(debug=True, port=8888)
