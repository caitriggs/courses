import os, sys, shutil
import numpy as np
from collections import defaultdict
from glob import glob


'''
Supporting functions for creating, moving, and copying files in directories
'''

def make_dirs(path, classes, sample=''):
    '''
    path (str): the absolute path to your parent data folder in which you want to make new subdirs
    classes (list): the names of the image classes (e.g. ['dog', 'cat'])
    sample (str): By default creates the regular train and valid directories. 
        Use sample='sample/' to create sample directories
    '''
    # make class subdirs if they don't already exist
    # relative path didn't work here, so use os.getcwd() and prepend to path --> path = os.getcwd() + '/path/to/data/'
    for clas in classes: 
        t_cls_dir = os.path.dirname(path + sample + '/train/' + clas + '/')
        v_cls_dir = os.path.dirname(path + sample + '/valid/' + clas + '/')
        if not os.path.exists(t_cls_dir):
            os.makedirs(t_cls_dir)
        if not os.path.exists(v_cls_dir):
            os.makedirs(v_cls_dir)
    # create a sub test directory for the sample directory
    if sample == 'sample/':
        test_cls_dir = os.path.dirname(path + sample + '/test/test_sub/')
        if not os.path.exists(test_cls_dir):
            os.makedirs(test_cls_dir)
    return None


def count_files(path, classes, sample='', train='train/'):
    '''
    path (str): the absolute path to your parent data folder in which you want to make new subdirs
    classes (list): the names of the image classes (e.g. ['dog', 'cat'])
    sample (str): by default looks in the regular train directory to count the # of files in the train directory
        Use sample='sample' to count in sample directories
    train (str): by default looks in the regular train directory. Change to 'valid/' to count # of files in valid directory
    '''
    # Find number of files already in the train directory
    class_dict = defaultdict(int)
    file_sum = 0
    for clas in classes:
        joined_path = path + sample + train + clas
        length = len([name for name in os.listdir(joined_path) if os.path.isfile(os.path.join(joined_path, name))])
        class_dict[clas] = length
        file_sum += length
    return class_dict, file_sum


def add_trailing_slash(path):
    '''
    path (str): the absolute path to your parent data folder in which you want to make new subdirs
    '''
    # just make sure there's a trailing slash so things concat nicely
    if path[-1] != '/':
        path += '/'
    return path


def find_split(file_list, train_split):
    '''
    file_list (list): the list of file paths in the train directory
    returns the index (int) where the train/valid split should occur. 
        this index marks the beginning of the validation set that will be moved out of train
    '''
    return int(len(file_list) * train_split)


'''
        Create Train and Valid Directories: move all class subdirectories of appropriate split to new valid directory
'''

def create_train_val_dirs(path, classes, train_split=0.80):
    '''
    path (str): the absolute path to your parent data folder in which you want to make new subdirs
    classes (list): the names of the image classes (e.g. ['dog', 'cat'])
    train_split (float): the percentage (0-1.0) of the training set that will be used to calculate how many images
        will be in the new training set (validation size will be 1 - train_split)
    '''
    # just make sure there's a trailing slash so things concat nicely
    path = add_trailing_slash(path)

    # Create sample subdirectories
    make_dirs(path, classes)

    # Get number of files already in valid directories if any
    class_dict, file_sum = count_files(path, classes, train='valid/')

    if file_sum == 0:
        g = glob(path + 'train/' + 'c?/*.jpg')
        # Find index split 
        index = find_split(g, train_split)
        # Move a random sample of images from train to valid
        shuffled = np.random.permutation(g)[index:]
        for _, f in enumerate(shuffled):
            f_name = '/'.join(f.split('/')[-2:])
            shutil.move(f, path + 'valid/' + f_name)
        print("Validation files moved from training directory.\n\
            Train size: {}\nValidation size: {}".format(train_split, 1-train_split))
    else:
        print("Validation directories already contain files")

'''
        Create Sample Directory: copy images to new train, valid and test subdirectories
'''

def copy_train_imgs(path):
    # Copy a random sample of 1500 images from train to sample train
    g = glob(path + 'train/' + 'c?/*.jpg')
    shuffled = np.random.permutation(g)[:1500]

    for _, f in enumerate(shuffled):
        f_name = '/'.join(f.split('/')[-2:])
        shutil.copyfile(f, path + 'sample/train/' + f_name)
    return None


def copy_valid_imgs(path):
    # Copy a random sample of 1000 images from validation to sample valid
    g = glob(path + 'valid/' + 'c?/*.jpg')
    shuffled = np.random.permutation(g)[:1000]

    for _, f in enumerate(shuffled):
        f_name = '/'.join(f.split('/')[-2:])
        shutil.copyfile(f, path + 'sample/valid/' + f_name)
    return None


def copy_test_imgs(path):
    # Copy a random sample of 1000 images from test to sample test
    g = glob(path + 'test/test_sub/' + '*.jpg')
    shuffled = np.random.permutation(g)[:1000]

    for _, f in enumerate(shuffled):
        f_name = '/'.join(f.split('/')[-1:])
        shutil.copyfile(f, path + 'sample/test/test_sub/' + f_name)
    return None


def create_sample_dirs(path, classes):
    '''
    path (str): the absolute path to your parent data folder in which you want to make new subdirs
    classes (list): the names of the image classes (e.g. ['dog', 'cat'])
    '''
    # just make sure there's a trailing slash so things concat nicely
    path = add_trailing_slash(path)

    # Create sample subdirectories
    make_dirs(path, classes, sample='sample/')

    # Get number of files already in sample directories if any
    class_dict, file_sum = count_files(path, classes, sample='sample/')

    # If sample direcotry doesn't already have files in it, create copies of files for train, valid and test directories
    if file_sum == 0:
        # Copy a random sample of 1500 images from train to sample train
        copy_train_imgs(path)
        # Copy a random sample of 1000 images from validation to sample valid
        copy_valid_imgs(path)
        # Copy a random sample of 1000 images from test to sample test
        copy_test_imgs(path)
        print("Samples directories created with copies of files for train and validation\nSample test directory created")
    else:
        print("Sample directories already contain files")


if __name__ == '__main__':
    pass