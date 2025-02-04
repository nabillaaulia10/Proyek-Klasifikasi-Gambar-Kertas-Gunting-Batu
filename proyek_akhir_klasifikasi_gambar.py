# -*- coding: utf-8 -*-
"""Proyek Akhir : Klasifikasi Gambar.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mi0DvyQ1K866nSPsskZYaqzYCycislea
"""

# download dataset using wget command
!wget --no-check-certificate \
  https://github.com/dicodingacademy/assets/releases/download/release/rockpaperscissors.zip

import os
import zipfile

local_zip = 'rockpaperscissors.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('rockpaperscissors')
zip_ref.close()

os.listdir('rockpaperscissors/rockpaperscissors')

base_dir = ('rockpaperscissors/rockpaperscissors/rps-cv-images')

paper = os.path.join('rockpaperscissors/rockpaperscissors/paper')
rock = os.path.join('rockpaperscissors/rockpaperscissors/rock')
scissors = os.path.join('rockpaperscissors/rockpaperscissors/scissors')

train_paper = os.listdir(paper)
train_rock = os.listdir(rock)
train_scissors= os.listdir(scissors)
print('Total training paper Images:', len(train_paper))
print('Total training rock Images:', len(train_rock))
print('Total training scissors Images:', len(train_scissors))

"""Data Pre-processing"""

import os

# Ganti dengan jalur absolut ke folder 'train'
train_dir = os.path.abspath('rockpaperscissors/rockpaperscissors/rps-cv-images')

# Cek apakah jalur tersebut valid
if not os.path.exists(train_dir):
    print(f"Jalur tidak ditemukan: {train_dir}")
else:
    print(f"Jalur valid: {train_dir}")

from tensorflow.keras.preprocessing.image import ImageDataGenerator

import tensorflow as tf
print(tf.__version__)

!pip show tensorflow

train_datagen = ImageDataGenerator(
                    rescale=1./255,
                    rotation_range=20,
                    horizontal_flip=True,
                    shear_range=0.2,
                    zoom_range=0.2,
                    fill_mode = 'nearest',
                    # Data is divided into 40% data validation and 60% training data
                    validation_split=0.4)

train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(150, 150),
        batch_size=40,
        class_mode='categorical',
        subset='training')

validation_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(150, 150),
        batch_size=40,
        class_mode='categorical',
        subset='validation')

"""Shoping image examples"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg  # Mengganti mping menjadi mpimg

# Menunjukkan gambar dalam format 5x5
nrows = 5
ncols = 5

# Indeks iterasi
pic_index = 0

# Membuat objek gambar
fig = plt.figure()
fig.set_size_inches(ncols * 5, nrows * 5)

pic_index += 8

# Mendapatkan path gambar untuk kategori paper, rock, dan scissors
next_paper_pix = [os.path.join(paper, fname) for fname in train_paper[pic_index - 8:pic_index]]
next_rock_pix = [os.path.join(rock, fname) for fname in train_rock[pic_index - 8:pic_index]]
next_scissors_pix = [os.path.join(scissors, fname) for fname in train_scissors[pic_index - 8:pic_index]]

for i, img_path in enumerate(next_paper_pix + next_rock_pix + next_scissors_pix):
  sp = plt.subplot(nrows, ncols, i+1)
  sp.axis('off')

  img = mpimg.imread(img_path)  # Menggunakan mpimg.imread untuk membaca gambar
  plt.imshow(img)

plt.show()

"""CNN architecture"""

from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint
import tensorflow as tf

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(64, (3,3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.summary()

"""Compile the pre-built model"""

history = model.fit(
    train_generator,
    steps_per_epoch = 41, # 1312 images = batch_size * steps
    epochs = 20,
    validation_data = validation_generator,
    validation_steps = 27, # 876 images = batch_size * steps
    verbose =2,
      callbacks=[callbacks]
)

class stop(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy')>0.96):
      print("\nAccuracy has reached 0.96")
      self.model.stop_training=True
callbacks=stop()
# train models with model.fit
train_models = model.fit(
      train_generator,
      batch_size=15,
      epochs=10,
      validation_data=validation_generator,
      validation_steps=5,
      callbacks=[callbacks])

plt.plot(history.history['loss'], label='Train')
plt.plot(history.history['val_loss'], label='Validation')
plt.legend()

plt.plot(history.history['accuracy'], label='Train')
plt.plot(history.history['val_accuracy'], label='Validation')
plt.legend()

"""Upload and predict an image"""

from google.colab import files
from keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt

# Upload file
uploaded = files.upload()

for fn in uploaded.keys():
    # Predicting images
    path = fn
    img = image.load_img(path, target_size=(150, 150))
    imgplot = plt.imshow(img)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    images = np.vstack([x])
    classes = model.predict(images, batch_size=10)

    print(fn)
    if classes[0, 0] != 0:
        print('This picture shows the shape of the paper')
    elif classes[0, 1] != 0:
        print('This picture shows the shape of the rock')
    elif classes[0, 2] != 0:
        print('This picture shows the shape of the scissors')
    else:
        print('Unknown image')