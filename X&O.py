import matplotlib.pyplot as plt
from tensorflow.keras.layers import Flatten
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras.layers import Dense  
from tensorflow.keras.layers import Conv2D
from tensorflow.random import normal
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.models import Sequential 
from tensorflow.keras.optimizers import Adam 
from tensorflow.keras import utils  
from keras.utils import np_utils
from tensorflow.keras.preprocessing import image 
import numpy as np
import os
import matplotlib.pyplot as plt 
from PIL import Image 
# %matplotlib inline

# Загрузка датасета из облака
import gdown
gdown.download('https://storage.yandexcloud.net/aiueducation/Content/base/l3/hw_pro.zip', None, quiet=True)

# Распаковываем архив hw_light.zip в папку hw_light
!unzip -q hw_pro.zip

# Путь к директории с базой
base_dir = '/content/hw_pro'
# Создание пустого списка для загрузки изображений обучающей выборки
x_train = []
# Создание списка для меток классов
y_train = []
# Задание высоты и ширины загружаемых изображений
img_height = 20
img_width = 20
# Перебор папок в директории базы
for patch in os.listdir(base_dir):
    # Перебор файлов в папках
    for img in os.listdir(base_dir + '/' + patch):
        # Добавление в список изображений текущей картинки
        x_train.append(image.img_to_array(image.load_img(base_dir + '/' + patch + '/' + img,
                                                         target_size=(img_height, img_width),
                                                         color_mode='grayscale')))
        # Добавление в массив меток, соответствующих классам
        if patch == '0':
            y_train.append(0)
        else:
            y_train.append(1)
# Преобразование в numpy-массив загруженных изображений и меток классов
x_train = np.array(x_train)
y_train = np.array(y_train)
# Вывод размерностей
# Вывод формы данных для обучения

# Номер картинки
n = 65
# Отрисовка картинки
plt.imshow(np.squeeze(x_train[0], 2))
# Вывод n-й картинки
plt.show()

# Преобразование x_train в тип float32 (числа с плавающей точкой) и нормализация
x_train = x_train / 255.0
# Преобразование y_train в тип float32 (числа с плавающей точкой) и нормализация
y_train = y_train / 255.0

y_train = np_utils.to_categorical(y_train)
x_train = np_utils.to_categorical(x_train)

print('Размер массива x_train', x_train.shape)
print('Длинна массива y_train', y_train.shape)

CLASS_COUNT = 2
class_names = ['X', 'O']

#x_train = np.random.rand(102,20,20,2)
#y_train = np.random.rand(102,2)

model = Sequential([
    Flatten(input_shape=(20,20,2)),
    Dense(512, activation='relu'),
    Dense(CLASS_COUNT,activation='softmax') 
])

model.compile(
    #loss=BinaryCrossentropy(from_logits=True), 
    loss='sparse_categorical_crossentropy',
    optimizer='adam', metrics=['accuracy'])
print(model)

model.fit(x_train, y_train, epochs=50, steps_per_epoch=200, verbose=1)
test_loss, test_acc = model.evaluate(x_train,  y_train, verbose=2)
print('\nTest accuracy:', test_acc)

n_rec = np.random.randint(x_train.shape[0])
x = x_train[n_rec]
x = np.expand_dims(x, axis=0)
prediction = model.predict(x)
pred = np.argmax(prediction)
print('Распознано: ')
if pred == 0:
  print('O')
else:
  print('X')
print('Правильный ответ: ')
if y_train[n_rec] == 0:
  print('O')
else:
  print('X')
