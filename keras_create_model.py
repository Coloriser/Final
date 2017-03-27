from __future__ import print_function
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D, Convolution2D
from keras.layers.convolutional import ZeroPadding2D
from keras import backend as K
from keras import regularizers

# from keras.callbacks import ModelCheckpoint


import numpy as np
import argparse

import sys
sys.path.insert(0, './helper_modules')
import helper_functions as hf

batch_size = 128
num_classes = 10
epochs = 12

def parse_arguments():						#argument parser -d for the pathlist
	parser = argparse.ArgumentParser(description='Trains the model, to be used after running pre-works')
	parser.add_argument('-a', help='to train based on a-channel', required=False,action="store_true", default=False)
	parser.add_argument('-b', help='to train based on b-channel', required=False,action="store_true", default=False)
	args = parser.parse_args()
	return args

def prereq_load_and_compute( mode , SIFT=False):
	# if SIFT==True:
		# print("SIFT")
		# paths = hf.load_sift_paths('train')
	# else:
		# print("BRISK")
		# paths = hf.load_brisk_paths('train')
	# print("loading features...")
	# features = hf.load_features(paths)
	# print(str(len(features)) + " items loaded.")	
	# print("Normalizing features")
	# modified_feature_arr = hf.normalize_array(features)
	# No_Of_Test_Items = len(modified_feature_arr)

	l_channel_paths = hf.load_luminance_paths('train')
	print("Loading Luma")
	l_channel_chromas = hf.load_luminance(l_channel_paths)
	print(str(len(l_channel_chromas)) + " items loaded.")
	modified_feature_arr = l_channel_chromas
	No_Of_Test_Items = len(modified_feature_arr)
	

	
	if mode=='a':
		a_channel_paths = hf.load_a_channel_chroma_paths('train')
		print("loading a channel chroma...")
		a_channel_chromas = hf.load_a_channel_chroma(a_channel_paths)
		# print(a_channel_chromas[0])
		# print(a_channel_chromas[1])
		print(str(len(a_channel_chromas)) + " items loaded.")	
		train_y_channel = np.array(a_channel_chromas).reshape(No_Of_Test_Items,-1)

	else:	
		b_channel_paths = hf.load_b_channel_chroma_paths('train')
		print("loading b channel chroma...")
		b_channel_chromas = hf.load_b_channel_chroma(b_channel_paths)
		print(str(len(b_channel_chromas)) + " items loaded.")
		train_y_channel = np.array(b_channel_chromas).reshape(No_Of_Test_Items, -1)

	train_y_channel = train_y_channel+128
	train_y_channel = train_y_channel/256.0

	print("modifying the shape of input and output")
	train_x = np.array(modified_feature_arr).reshape([No_Of_Test_Items, modified_feature_arr[0].shape[0], modified_feature_arr[0].shape[1], 1])
	
	print("Pickling shapes")
	hf.pickle_shape(train_x,train_y_channel)

	print("train_x shape: ",train_x.shape)
	print("train_y shape: ",train_y_channel.shape)

	return train_x, train_y_channel


# input image dimensions
# img_rows, img_cols = 28, 28


def make_model(x_train, y_train, filename):


	model = Sequential()

	model.add(Convolution2D(32, 3, 1, activation='relu', input_shape=(x_train.shape[1], x_train.shape[2], 1), activity_regularizer=regularizers.l1(0.01)))
	model.add(Convolution2D(32, 3, 1, activation='relu',activity_regularizer=regularizers.l1(0.01)))
	model.add(Convolution2D(32, 3, 1, activation='relu',activity_regularizer=regularizers.l1(0.01)))
	model.add(Convolution2D(32, 3, 1, activation='relu',activity_regularizer=regularizers.l1(0.01)))
	model.add(Convolution2D(32, 1, 1, activation='relu',activity_regularizer=regularizers.l1(0.01)))
	model.add(Convolution2D(32, 1, 1, activation='relu',activity_regularizer=regularizers.l1(0.01)))
	model.add(Convolution2D(32, 1, 1, activation='relu',activity_regularizer=regularizers.l1(0.01)))
	model.add(Convolution2D(32, 1, 1, activation='relu',activity_regularizer=regularizers.l1(0.01)))
	model.add(Convolution2D(32, 1, 1, activation='relu',activity_regularizer=regularizers.l1(0.01)))
	model.add(Convolution2D(32, 1, 1, activation='sigmoid',activity_regularizer=regularizers.l1(0.01)))
	model.add(Flatten())
	model.add(Dense(128	, activation='sigmoid'))
	model.add(Dense(40000, activation='sigmoid'))



	# model.add(MaxPooling2D(pool_size=(2,2)))
	# model.add(Dropout(0.25))

	# model.add(Flatten())
	# model.add(Dense(128, activation='relu'))
	# model.add(Dropout(0.5))
	# model.add(Dense(40000, activation='sigmoid'))

# model = Sequential()
	# model.add(ZeroPadding2D((1,1), input_shape=(x_train.shape[1], x_train.shape[2], 1)))
	# model.add(Convolution2D(64, 3, 3, activation='sigmoid'))
	# model.add(ZeroPadding2D((1,1)))
	# model.add(Convolution2D(64, 3, 3, activation='sigmoid'))
	# model.add(MaxPooling2D((2,2), strides=(2,2)))
	# model.add(ZeroPadding2D((1,1)))
	# model.add(Convolution2D(128, 3, 3, activation='sigmoid'))
	# model.add(ZeroPadding2D((1,1)))
	# model.add(Convolution2D(128, 3, 3, activation='sigmoid'))
	# model.add(MaxPooling2D((2,2), strides=(2,2)))
	# model.add(ZeroPadding2D((1,1)))
	# model.add(Convolution2D(256, 3, 3, activation='sigmoid'))
	# model.add(ZeroPadding2D((1,1)))
	# model.add(Convolution2D(256, 3, 3, activation='sigmoid'))
	# model.add(ZeroPadding2D((1,1)))
	# model.add(Convolution2D(256, 3, 3, activation='sigmoid'))
	# model.add(MaxPooling2D((2,2), strides=(2,2)))
	# model.add(ZeroPadding2D((1,1)))
	# model.add(Convolution2D(512, 3, 3, activation='sigmoid'))
	# model.add(ZeroPadding2D((1,1)))
	# model.add(Convolution2D(512, 3, 3, activation='sigmoid'))
	# model.add(ZeroPadding2D((1,1)))
	# model.add(Convolution2D(512, 3, 3, activation='sigmoid'))
	# model.add(MaxPooling2D((2,2), strides=(2,2)))
	# model.add(ZeroPadding2D((1,1)))
	# model.add(Convolution2D(512, 3, 3, activation='sigmoid'))
	# model.add(ZeroPadding2D((1,1)))
	# model.add(Convolution2D(512, 3, 3, activation='sigmoid'))
	# model.add(ZeroPadding2D((1,1)))
	# model.add(Convolution2D(512, 3, 3, activation='sigmoid'))
	# model.add(MaxPooling2D((2,2), strides=(2,2)))
	# model.add(Flatten())
	# model.add(Dense(4096, activation='sigmoid'))
	# model.add(Dropout(0.5))
	# model.add(Dense(4096, activation='sigmoid'))
	# model.add(Dropout(0.5))
	# model.add(Dense(40000, activation='sigmoid'))



	model.compile(loss='categorical_crossentropy',
				  optimizer='adam',
				  metrics=['accuracy'])

	# checkpointer = ModelCheckpoint(filename, monitor='val_loss', verbose=0, save_best_only=False, save_weights_only=False, mode='auto', period=5)
	model.fit(x_train, y_train, 
			  batch_size=32, nb_epoch=10, verbose=1
			  # , callbacks=[checkpointer]
			  )

	model.save(filename)

	return


def make_a_model(  ):
	filename = "model/a_channel.model"

	print("Generating A channel model")

	train_x, train_y_a_channel = prereq_load_and_compute( mode='a' , SIFT=True)

	make_model(train_x, train_y_a_channel, filename)

def make_b_model():
	filename = "model/b_channel.model"

	print("Generating B channel model")

	train_x, train_y_b_channel = prereq_load_and_compute( mode='b' , SIFT=True)

	make_model( train_x, train_y_b_channel, filename)

def main():
	args = parse_arguments()
	# print(args)
	if args.a:
		print("Training model based on a-channel")
		make_a_model()
	if args.b:	
		print("Training model based on b-channel")
		make_b_model()
	if not args.a and not args.b:
		print("ERROR: use -h for HELP")

main()
