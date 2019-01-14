from keras.models import Sequential
from keras.layers import Dense
import numpy as np
from numpy import genfromtxt

# fix random seed for reproducibility
np.random.seed(7)
# load pima indians dataset
X 	= genfromtxt('data_X.csv', delimiter=',',skip_header=1)
Y_f = genfromtxt('data_Y.csv', delimiter=',',skip_header=1)
Y	= np.rint(Y_f)
# create model
model = Sequential()
model.add(Dense(16, input_dim=12, activation='relu'))
model.add(Dense(12, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# Fit the model
model.fit(X, Y, epochs=30, batch_size=10, verbose=2)
# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

predictions=model.predict(X)
dev=0.0
for i in range(100):
	dev+=abs(Y_f[i]-predictions[i])
	print(Y_f[i],predictions[i])
print("average deviation",dev/100.0)
