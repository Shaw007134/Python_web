from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, flash, url_for, redirect, render_template
from PIL import Image
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.image import imread, imsave
from skimage.transform import resize

depth_data = np.genfromtxt('./img.csv', delimiter=',', skip_header=1, skip_footer=1, usecols=range(1,201))
print(depth_data.shape)
print(depth_data[0][0], depth_data[-1][0])



# imsave('./original_depth.png', depth_data, cmap='gray')
plt.imshow(depth_data)
# resized_data = resize(depth_data, (150,  depth_data.shape[0]))

# fig, axes = plt.subplots(nrows=2, ncols=2)

# ax = axes.ravel()

# ax[0].imshow(resized_data, cmap='gray')
# ax[0].set_title("Original image")

# im = Image.open(r'./original_depth.png')
# im.show()
# width, height = im.size
# print(width, height)

# im1 = im.resize((150, height), resample=2)
# im1.save('./resized_depth.png')
# im1.show()

# im_df = pd.DataFrame(im1)
# print(type(im_df))



# host = '127.0.0.1'
# port = 3306
# db = 'depth'
# user = 'root'
# password = 'root'

# app = Flask(__name__)
# app.config['SQLAlchemy_DATABASE_URI'] = str(r"mysql+pymysql://%s:" + '%s' + "@%s/%s") % (user, password, host, db)


# db = SQLAlchemy(app)

# class Layer(db.Model):
#   id = db.Column('id', db.Integer, primary_key = True)
#   name = db.Column(db.String(100))
#   age = db.Column(db.String(200))
