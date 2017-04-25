from glob import glob
from os.path import exists, join, basename, splitext
import helper_functions as hf

EXTENSIONS = [".jpg",".png"]

def get_image_paths(path="dataset/train"):
	"""Get the list of all image files in the train directory"""
	image_paths = []
	image_paths.extend([join(path, basename(fname))
					for fname in glob(path + "/*")
					if splitext(fname)[-1].lower() in EXTENSIONS])
	return image_paths

def refineName( fullname ):
	return fullname.split('/')[-1].split('.')[0] 


def getAndFilterPaths( ):
	path = "./predicted_images/"
	out = get_image_paths(path)
	final = []
	for path in out:
		if '_AB' in path:
			final.append(path)
	return final		
