import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
import numpy as np
from keras.datasets import mnist
import matplotlib.pyplot as plt
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
#checkout the data
from keras.utils import to_categorical
import pickle as pickle
from keras.callbacks import ModelCheckpoint, EarlyStopping
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense



gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # Restrict TensorFlow to only use the fourth GPU
        tf.config.experimental.set_visible_devices(gpus[0], 'GPU')

        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)
X = np.array(pickle.load(open("C:/Users/USER/Desktop/NeuralNetwork/CatDogs/X.pickle","rb")))
y = np.array(pickle.load(open("C:/Users/USER/Desktop/NeuralNetwork/CatDogs/y.pickle","rb")))

train_images = X
train_labels = y
test_images = X
test_labels = y

print('Training data shape : ', train_images.shape, train_labels.shape)

print('Testing data shape : ', test_images.shape, test_labels.shape)
# Find the unique numbers from the train labels
classes = np.unique(train_labels)
nClasses = len(classes)
print('Total number of outputs : ', nClasses)
print('Output classes : ', classes)

plt.figure(figsize=[10,5])

# Display the first image in training data
plt.subplot(121)
plt.imshow(train_images[0,:,:,0], cmap='gray')
plt.title("Ground Truth : {}".format(train_labels[0]))

# Display the first image in testing data
plt.subplot(122)
plt.imshow(test_images[1,:,:,0], cmap='gray')
plt.title("Ground Truth : {}".format(test_labels[1]))
#plt.show()

# Change from matrix to array of dimension 50x50 to array of dimention 784
dimData = np.prod(train_images.shape[1:])
train_data = train_images.reshape(train_images.shape[0], dimData)
test_data = test_images.reshape(test_images.shape[0], dimData)

# Change to float datatype
train_data = train_data.astype('float32')
test_data = test_data.astype('float32')

# Scale the data to lie between 0 to 1
train_data /= 255
test_data /= 255

# Change the labels from integer to categorical data
train_labels_one_hot = to_categorical(train_labels)
test_labels_one_hot = to_categorical(test_labels)

# Display the change for category label using one-hot encoding
print('Original label 0 : ', train_labels[0])
print('After conversion to categorical ( one-hot ) : ', train_labels_one_hot[0])

from keras.models import Sequential
from keras.layers import Dense

from keras.layers import Dropout

model_reg = Sequential()
model_reg.add(Dense(512, activation='relu', input_shape=(dimData,)))
model_reg.add(Dropout(0.5))
model_reg.add(Dense(512, activation='relu'))
model_reg.add(Dropout(0.5))
model_reg.add(Dense(nClasses, activation='softmax'))

model_reg.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
es = EarlyStopping(monitor='val_loss', mode='min', verbose=1)
history_reg = model_reg.fit(train_data, train_labels_one_hot, batch_size=256, epochs=5000000, verbose=1,
                            validation_data=(test_data, test_labels_one_hot))

#Plot the Loss Curves
plt.figure(figsize=[8,6])
plt.plot(history_reg.history['loss'],'r',linewidth=3.0)
plt.plot(history_reg.history['val_loss'],'b',linewidth=3.0)
plt.legend(['Training loss', 'Validation Loss'],fontsize=18)
plt.xlabel('Epochs ',fontsize=16)
plt.ylabel('Loss',fontsize=16)
plt.title('Loss Curves',fontsize=16)

#Plot the Accuracy Curves
plt.figure(figsize=[8,6])
plt.plot(history_reg.history['accuracy'],'r',linewidth=3.0)
plt.plot(history_reg.history['val_accuracy'],'b',linewidth=3.0)
plt.legend(['Training Accuracy', 'Validation Accuracy'],fontsize=18)
plt.xlabel('Epochs ',fontsize=16)
plt.ylabel('Accuracy',fontsize=16)
plt.title('Accuracy Curves',fontsize=16)

# Predict the most likely class
model_reg.predict_classes(test_data[[0],:])
print(model_reg.predict_classes(test_data[[0],:]))

# Predict the probabilities for each class
model_reg.predict(test_data[[0],:])
print(model_reg.predict(test_data[[0],:]))



plt.imshow(test_images[2,:,:,0], cmap='gray')
plt.title("Ground Truth : {}".format(test_labels[2]))


# Predict the most likely class
model_reg.predict_classes(test_data[[2],:])
print(model_reg.predict_classes(test_data[[2],:]))
# Predict the probabilities for each class
model_reg.predict(test_data[[2],:])
print(model_reg.predict(test_data[[2],:]))

model_reg.save("model.h5")
print("Saved model to disk")

plt.show()

