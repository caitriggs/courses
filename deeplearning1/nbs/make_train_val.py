import os, sys, shutil
import numpy as np
from collections import defaultdict
from glob import glob


def make_dirs(path, classes, sample=''):
    '''
    path (str): the absolute path to your parent data folder in which you want to make new subdirs
    classes (list): the names of the image classes (e.g. ['dog', 'cat'])
    '''
    # make class subdirs if they don't already exist (relative path didn't work here, so added os.getcwd())
    for clas in classes: 
        t_cls_dir = os.path.dirname(path + sample + '/train/' + clas + '/')
        v_cls_dir = os.path.dirname(path + sample + '/valid/' + clas + '/')
        if not os.path.exists(t_cls_dir):
            os.makedirs(t_cls_dir)
        if not os.path.exists(v_cls_dir):
            os.makedirs(v_cls_dir)
    return None


def count_files(path, classes, sample='', train='train/'):
    '''
    path (str): the absolute path to your parent data folder in which you want to make new subdirs
    classes (list): the names of the image classes (e.g. ['dog', 'cat'])
    sample (str): by default looks in the regular train directory to count the # of files in the train directory
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


def create_sample_dirs(path, classes):
    '''
    path (str): the absolute path to your parent data folder in which you want to make new subdirs
    classes (list): the names of the image classes (e.g. ['dog', 'cat'])
    '''
    # just make sure there's a trailing slash so things concat nicely
    path = add_trailing_slash(path)

    # Create sample subdirectories
    make_dirs(path, classes, sample='sample/')
    # Training image directory path
    train_path = path + 'train/'

    # Get number of files already in sample directories if any
    class_dict, file_sum = count_files(path, classes, sample='sample/')

    if file_sum == 0:
        g = glob(train_path + 'c?/*.jpg')
        
        # Copy a random sample of images for train
        shuffled = np.random.permutation(g)[:1500]
        for _, f in enumerate(shuffled):
            f_name = '/'.join(f.split('/')[-2:])
            shutil.copyfile(f, path + 'sample/train/' + f_name)

        # Copy a random sample of images for validation
        shuffled = np.random.permutation(g)[:1000]
        for _, f in enumerate(shuffled):
            f_name = '/'.join(f.split('/')[-2:])
            shutil.copyfile(f, path + 'sample/valid/' + f_name)
        print("Samples directories created with copies of files for train and validation")
    else:
        print("Sample directories already contain files")


def create_train_val_dirs(path, classes, train_split=0.80):
    '''
    path (str): the absolute path to your parent data folder in which you want to make new subdirs
    classes (list): the names of the image classes (e.g. ['dog', 'cat'])
    '''
    # just make sure there's a trailing slash so things concat nicely
    path = add_trailing_slash(path)

    # Create sample subdirectories
    make_dirs(path, classes)
    # Training image directory path
    train_path = path + 'train/'

    # Get number of files already in valid directories if any
    class_dict, file_sum = count_files(path, classes, train='valid/')

    if file_sum == 0:
        g = glob(train_path + 'c?/*.jpg')
        
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


if __name__ == '__main__':
    pass