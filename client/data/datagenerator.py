import numpy as np
import tensorflow.keras as keras
import os
class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, list_IDs, labels, data_path,  batch_size=32, dim=(100,100), n_channels=4,
                 n_classes=15, shuffle=True):
        'Initialization'
        self.dim = dim
        self.batch_size = batch_size
        self.labels = labels
        self.list_IDs = list_IDs
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.on_epoch_end()
        self.data_path = data_path

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.list_IDs) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]
        # Find list of IDs
        list_IDs_temp = [self.list_IDs[k] for k in indexes]

        # Generate data
        X, y = self.__data_generation(list_IDs_temp)

        return X, y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.list_IDs))

        if self.shuffle == True:
            np.random.shuffle(self.indexes)


    def __data_generation(self, list_IDs_temp):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        # Initialization
        X = np.empty((self.batch_size, *self.dim, self.n_channels))
        y = np.empty((self.batch_size,), dtype=int)
        # Generate data
        for i, ID in enumerate(list_IDs_temp):
            # Store sample
            X[i,] = np.load(os.path.join(self.data_path, ID + '.npy'))
            # Store class
            y[i] = self.labels[ID]


        return X, keras.utils.to_categorical(y, num_classes=self.n_classes)

    def predict_all(self, model):

        preds = np.empty((len(self.list_IDs), self.n_classes))
        labels = np.empty((len(self.list_IDs), self.n_classes))
        for index in range(self.__len__()):
            indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]
            list_IDs_temp = [self.list_IDs[k] for k in indexes]
            X, y = self.__data_generation(list_IDs_temp)
            labels[index*self.batch_size:(index+1)*self.batch_size,] = y
            preds[index*self.batch_size:(index+1)*self.batch_size,] = model.predict(X)

        # extract the last examples
        index = self.__len__()
        indexes = self.indexes[index * self.batch_size:]
        list_IDs_temp = [self.list_IDs[k] for k in indexes]
        X, y = self.__data_generation(list_IDs_temp)
        labels[index * self.batch_size:, ] = y[:len(indexes)]
        preds[index * self.batch_size:, ] = model.predict(X[:len(indexes)])

        return labels, preds

