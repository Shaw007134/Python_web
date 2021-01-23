from sqlalchemy import create_engine
from flask import Flask, request, flash, url_for, redirect, render_template
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt 
from matplotlib.image import imread, imsave
from skimage.transform import resize

host = '127.0.0.1'
port = 3306
db = 'depth'
user = 'root'
password = 'zsy007'

depth_data = np.genfromtxt('./img.csv', delimiter=',', skip_header = 1,  skip_footer=1, usecols=range(0,201))
print(depth_data.shape)
print(depth_data[:, 1:])
raw_data = depth_data[:, 1:]
imsave('original_data.png', raw_data)
plt.imshow(raw_data)

resized_data = resize(raw_data, (raw_data.shape[0], 150))
imsave('resized_data.png', resized_data)

resized_data = resized_data.astype(int)
out_data = np.concatenate((depth_data[:, 0:1], resized_data), axis=1)

columns = ['depth']
for i in range(150):
    columns.append('col' + str(i))
len(columns)


depth_df = pd.DataFrame(out_data, columns=columns)

engine = create_engine(str(r"mysql+mysqldb://%s:" + '%s' + "@%s/%s?charset=utf8") % (user, password, host, db))

try:
    depth_df.to_sql('layer',con=engine,if_exists='replace',index=False)
except Exception as e:
    print(e)

conn = engine.connect()

depth_min = 9100
depth_max = 9102

select_sql =r'SELECT * FROM layer WHERE depth > %d AND depth < %d ' % (depth_min, depth_max)
result = conn.execute(select_sql)
res = []
for row in result:
    res.append(row)
res_img = np.asarray(res)[:, 1:]
print(res_img.shape)

plt.imshow(res_img, cmap='gray')
imsave('r1.png', res_img, cmap='gray')


