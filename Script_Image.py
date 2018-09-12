import numpy as np
from glob import glob
from PIL import Image,ImageFilter
from sklearn import preprocessing
import argparse, os, shutil, random

import warnings
warnings.filterwarnings('ignore')

allowed_func=['get_data_with_multiscale_multiColorSpace',]

parser = argparse.ArgumentParser(description='Sundry scripts merge into a single file.')
parser.add_argument('--module', default='',
                    help='Choose which module name to use.\n%s' %",\n".join(allowed_func))
parser.add_argument('--data_dir', default='',
                    help='data_dir')
parser.add_argument('--train_flag', default=True, type=bool,
                    help='Train or test')
parser.add_argument('--save_dir', default='',
                    help='For save the numpy')

args = parser.parse_args()

def get_data_with_multiscale_multiColorSpace(data_dir=args.data_dir,
                                             save_dir=args.save_dir,
                                             train_flag=args.train_flag):
    '''
    :param data_dir:
            if train_flag == True:
               data-dir/dog/dog_1.jpg
               data-dir/dog/dog_2.jpg
               data-dir/cat/cat_1.jpg
               data-dir/cat/cat_1.jpg
            else:
               data-dir/test_1.jpg
               data-dir/test_2.jpg

    :param save_dir: save the numpy file. if train_flag which contain train_label.npy
    :return:
    '''

    multiscale = (224,299,384,512)
    multiColorSpace = ('1','L','HSV','CMYK','YCbCr')

    #multiscale = (224,299)
    #multiColorSpace = ('1')

    def more_from_one_image(img):
        cur_img_array = np.array(img)
        #print(cur_img_array.shape)
        for color in multiColorSpace:
            cl_img = np.array(img.convert(color))
            if len(cl_img.shape) != 3:
                cl_img = np.expand_dims(cl_img,axis=2) 
            cur_img_array = np.concatenate((cur_img_array,cl_img),axis=2)

        return cur_img_array

    def get_data_from_dir(cur_dir):
        cur_data_list = [[] for i in range(len(multiscale))]
        data_list = glob(cur_dir + '/*')
        for im_p in data_list:
            try:
                img_data = Image.open(im_p)  ##if not image,continue
            except:
                continue
            if img_data.mode != 'RGB':
                img_data = img_data.convert("RGB")
            for index,scale in enumerate(multiscale):
                resize_img = img_data.resize((scale,scale),Image.BILINEAR)
                more_img = more_from_one_image(resize_img)
                cur_data_list[index].append(more_img)
        return cur_data_list

    if train_flag:
        train_dir_name = []
        train_dir_number = []
        le = preprocessing.LabelEncoder()
        data_multiscale = [[] for i in range(len(multiscale))]
        for cur_dir in os.listdir(data_dir):
            cur_path = os.path.join(data_dir,cur_dir)
            if os.path.isdir(cur_path):
                cur_data_list = get_data_from_dir(cur_path)
                if len(cur_data_list[0]) > 0:
                    train_dir_name.append(cur_dir)
                    train_dir_number.append(len(cur_data_list[0]))
                    for index in range(len(multiscale)):
                        data_multiscale[index].extend(cur_data_list[index])
        print(len(train_dir_name))
        le.fit(train_dir_name)
        print(list(le.classes_))
        label_array = le.transform(train_dir_name)
        print(label_array)
        train_y = []
        for index in range(len(train_dir_name)):
            label_len = [label_array[index]] * train_dir_number[index]
            train_y.extend(label_len)
        print(len(train_y),len(data_multiscale[0]))
        assert len(train_y) == len(data_multiscale[0])
        np.save(save_dir + '/train_label.npy',np.array(train_y))
        pre_name = 'train'
    else:
        data_multiscale = get_data_from_dir(data_dir)
        pre_name = 'test'

    for index in range(len(multiscale)):
        np.save(save_dir + '/' + pre_name + '_' + str(multiscale[index]) + '.npy',np.array(data_multiscale[index]))

allowed_func={'get_data_with_multiscale_multiColorSpace':get_data_with_multiscale_multiColorSpace}
if __name__ == '__main__':
    if args.module in allowed_func:
         allowed_func[args.module]()
