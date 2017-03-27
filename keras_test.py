from __future__ import division, print_function, absolute_import

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D, Convolution2D
from keras import backend as K

from keras.models import load_model


import numpy as np
import pickle
import argparse

import sys
sys.path.insert(0, './helper_modules')
import helper_functions as hf

# import pre_works_test as pre_works

# x=[]
# y=[]
# to dp : https://github.com/shekkizh/Colorization.tensorflow



def parse_arguments():                      #argument parser -d for the pathlist
    parser = argparse.ArgumentParser(description='Tests the model, to be used after creating the model. To run in ab mode, run in -a and -b first')
    parser.add_argument("--path",'-p', help='the path to input (default: ./dataset/test)', required=False, default="./dataset/test")
    parser.add_argument('-a', help='to train based on a-channel', required=False,action="store_true", default=False)
    parser.add_argument('-b', help='to train based on b-channel', required=False,action="store_true", default=False)
    parser.add_argument('-ab', help='to train based on a&b-channel', required=False,action="store_true", default=False)
    args = parser.parse_args()
    return args    


def load_a_model():
    print("Loading 'a' model")
    return load_model("model/a_channel.model")

def load_b_model():
    print("Loading 'b' model")
    return load_model("model/b_channel.model")



def prereq_load_and_compute( SIFT=False):
    # print("Loading feature paths")
    # if SIFT==True:
    #     print("SIFT")
    #     paths = hf.load_sift_paths('test')

    # else:
    #     print("BRISK")
    #     paths = hf.load_brisk_paths('test')
    # print("loading features...")
    # features = hf.load_features(paths)
    # print(str(len(features)) + " items loaded.")    
    # print("Normalizing features")
    # modified_feature_arr = hf.normalize_array(features, mode = 'test')
    # No_Of_Test_Items = len(modified_feature_arr)    

    l_channel_paths = hf.load_luminance_paths('test')
    print("Loading Luma")
    l_channel_chromas = hf.load_luminance(l_channel_paths)
    print(str(len(l_channel_chromas)) + " items loaded.")
    modified_feature_arr = l_channel_chromas
    No_Of_Test_Items = len(modified_feature_arr)


    print("modifying the shape of input and output")
    test_x = np.array(modified_feature_arr).reshape([No_Of_Test_Items, modified_feature_arr[0].shape[0], modified_feature_arr[0].shape[1], 1])

    print("test_x shape: ",test_x.shape)

    return test_x

def predict_and_dump(test_x, mode):
    
    luminance_paths = hf.load_luminance_paths('test')
    print("loading luminance...")
    luminance = hf.load_luminance(luminance_paths)

    if mode=='a':
        b_channel_paths = hf.load_b_channel_chroma_paths('test')
        print("loading b channel chroma...")
        b_channel_chromas = hf.load_b_channel_chroma(b_channel_paths)
        # try:
        model = load_a_model()
        # except:
            # print("Error loading model")

    if mode=='b':    
        a_channel_paths = hf.load_a_channel_chroma_paths('test')
        print("loading a channel chroma...")
        a_channel_chromas = hf.load_a_channel_chroma(a_channel_paths)
        # try:
        model = load_b_model()
        # except:
            # print("Error loading model")

    predictions = model.predict(test_x)
    print("Dumping predictions")
    empty_array = np.zeros((200,200))
    if(mode == 'a'):
        hf.save_blob(predictions, 'predicted_a_chroma')
        for i in range(len(predictions)):
            a_channel_chroma = hf.scale_image(predictions[i])
            print("a_channel_chroma", a_channel_chroma)
            a_channel_chroma = a_channel_chroma*20
            hf.reconstruct(empty_array, a_channel_chroma,empty_array, i, 'A')
    if(mode == 'b'):
        hf.save_blob(predictions, 'predicted_b_chroma')    
        for i in range(len(predictions)):
            b_channel_chroma = hf.scale_image(predictions[i])
            b_channel_chroma = b_channel_chroma*20
            hf.reconstruct(empty_array, empty_array,b_channel_chroma, i, 'B')
    

def main():

    args = parse_arguments()
    DATASET_PATH = args.path
    mode = 'NONE'
    if not (args.a or args.b or args.ab): #Check if only one case is true
        print("ERROR: use -h for HELP")
        exit()
        return
    # print(args)
    if args.a:
        print("Testing model based on a-channel")
        mode = 'a'
    if args.b:  
        print("Testing model based on b-channel")
        mode = 'b'
    if args.ab:  
        print("Testing model based on a&b-channel")
        mode = 'ab'

    
    # FOR AKHEEL
    # print("processing images")
    # pre_works.process_images(DATASET_PATH)

    if(mode != 'ab') :   
        test_x = prereq_load_and_compute( SIFT = True )    
        predict_and_dump(test_x, mode)
        return

    # IF AB MODE
    print("Loading a_chroma")
    predictions_A = hf.load_from_pickle("predicted_a_chroma")
    print("a_channel_chroma", predictions_A[0][1])
    print("a_channel_chroma", predictions_A[1][1])
    print("a_channel_chroma", predictions_A[2][1])


    print("Loading b_chroma")
    predictions_B = hf.load_from_pickle("predicted_b_chroma")  
    luminance_paths = hf.load_luminance_paths('test')
    print("loading luminance...")
    luminance = hf.load_luminance(luminance_paths)
    for i in range(len(predictions_A)):
        a_channel_chroma = hf.scale_image(predictions_A[i])
        # print("a_channel_chroma", a_channel_chroma)
        b_channel_chroma = hf.scale_image(predictions_B[i])
        hf.reconstruct(luminance[i], a_channel_chroma,b_channel_chroma, i, 'AB')


main()        
