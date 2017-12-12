import os, sys
import shutil
from Counter import defaultdict

def make_dirs(path, classes):
    '''
    path (str): the absolute path to your parent data folder in which you want to make new subdirs
    classes (list): the names of the image classes (e.g. ['dog', 'cat'])
    '''
    # make class subdirs if they don't already exist (relative path didn't work here, so added os.getcwd())
    for clas in classes: 
        t_cls_dir = os.path.dirname(path+'/train/'+clas)
        v_cls_dir = os.path.dirname(path+'/valid/'+clas)
        if not os.path.exists(t_cls_dir):
            os.makedirs(t_cls_dir)
        if not os.path.exists(v_cls_dir):
            os.makedirs(v_cls_dir)
    return None


def create_sample_dirs(path, classes):
    '''
    path (str): the absolute path to your parent data folder in which you want to make new subdirs
    classes (list): the names of the image classes (e.g. ['dog', 'cat'])
    '''
    # just make sure there's a trailing slash so things concat nicely
    if path[-1] != '/':
        path += '/'

    # Create sample subdirectories
    make_dirs(path+'sample/', classes)

    train_path = path+'train/'    
    # Set number of files already in the train directory
    class_dict = defaultdict(int)
    for clas in classes:
        class_dict[clas] = len([name for name in os.listdir(path+'sample/train/'+clas) if os.path.isfile(os.path.join(path+'sample/train/'+clas, name))])
        
    
    for f in os.listdir(train_path):
        if f.split('.')[0] == 'dog' and dogs < 10:
            shutil.copy(train_path+f, path+'sample/train/dogs/')
            dogs += 1
        elif f.split('.')[0] == 'cat' and cats < 10:
            shutil.copy(train_path+f, path+'sample/train/cats/')
            cats += 1
    return [os.listdir(path+'sample/train/'+clas) for clas in class_dict]

