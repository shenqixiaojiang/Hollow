import json
import os
import random
import shutil
from multiprocessing import Pool, Manager

def copy_img(name,old_dir,new_dir,queue):
    shutil.copy(old_dir + name,new_dir + name)
    queue.put(name)

def copy(cur_path,save_dir):
    pool = Pool(20)
    queue = Manager().Queue()
    cp_data = list(os.listdir(cur_path))
    end = len(cp_data)
    for name in cp_data:
      pool.apply_async(copy_img, args=(name,cur_path,save_dir, queue))
      num = 0
      while True:
        queue.get()
        num += 1
        copyRate = num / float(end)
        print("\rcopy rate:%.2f%%" % (copyRate * 100))
        if num == end:
          break
