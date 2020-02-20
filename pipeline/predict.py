import model_modified as md
import os
import numpy as np
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tqdm import tqdm_notebook, tnrange
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img, save_img
from skimage.transform import resize
from skimage.morphology import label
import cv2
import sys
import time
#import matp
im_width = 128
im_height = 128

def read_images(image_path):
    ids = next(os.walk(image_path))[2] # list of names all images in the given path
    to_predict = np.zeros((len(ids), im_height, im_width, 1), dtype=np.float32)
    for n, id_ in tqdm_notebook(enumerate(ids), total=len(ids)):
        # Load images
        img = load_img(image_path + id_, color_mode = "grayscale")
        x_img = img_to_array(img)
        x_img = resize(x_img, (128, 128, 1), mode = 'constant', preserve_range = True)
        # Save images
        to_predict[n] = x_img/255.0
    return to_predict,ids

unet_model = md.get_model()
unet_model.compile(optimizer=Adam(), loss="binary_crossentropy", metrics=["accuracy"])

def predict_masks(images_npy, model, h5_path):
    model.load_weights(h5_path)
    predicted_masks = model.predict(images_npy,verbose=0)
    return predicted_masks

def mask_to_image(nerve,mask_npy,path_to_save,ids):
    
    path_to_save = path_to_save + "/" + nerve
    for i,item in enumerate(mask_npy):
        id = ids[i].split('.png')
        save_img(os.path.join(path_to_save,id[0]+"_"+nerve+"mask.png"),item)
        
def draw_contours(nerve , path_to_masks, path_to_images, path_to_save, ids):
    path_to_asm_masks = path_to_masks+'asm/'
    path_to_bp_masks = path_to_masks+'bp/'
    path_to_msm_masks = path_to_masks+'msm/'
    path_to_scm_masks = path_to_masks+'scm/'
    for i in range(len(next(os.walk(path_to_images))[2])):

        path_to_images1 = path_to_images + ids[i]
        original_image = cv2.imread(path_to_images1)
        shape = original_image.shape
        #asm
        id = ids[i].split('.png')
        nerve_mask = cv2.imread(path_to_asm_masks + id[0]+'_asmmask.png',cv2.IMREAD_GRAYSCALE)
        nerve_mask = cv2.resize(nerve_mask,(shape[0],shape[1]))
        asm_marked = contour_func(nerve_mask,original_image,ids[i],'asm',shape)
        #bp
        id = ids[i].split('.png')
        nerve_mask = cv2.imread(path_to_bp_masks + id[0]+'_bpmask.png',cv2.IMREAD_GRAYSCALE)
        nerve_mask = cv2.resize(nerve_mask,(shape[0],shape[1]))
        bp_marked = contour_func(nerve_mask,asm_marked,ids[i],'bp',shape)
        #scm
        id = ids[i].split('.png')
        nerve_mask = cv2.imread(path_to_scm_masks + id[0]+'_scmmask.png',cv2.IMREAD_GRAYSCALE)
        nerve_mask = cv2.resize(nerve_mask,(shape[0],shape[1]))
        scm_marked = contour_func(nerve_mask,bp_marked,ids[i],'scm',shape)
        #msm
        id = ids[i].split('.png')
        nerve_mask = cv2.imread(path_to_msm_masks + id[0]+'_msmmask.png',cv2.IMREAD_GRAYSCALE)
        nerve_mask = cv2.resize(nerve_mask,(shape[0],shape[1]))
        msm_marked = contour_func(nerve_mask,scm_marked,ids[i],'msm',shape)
        
        id = ids[i].split('.png')
        img_mask_name = path_to_save + id[0] +'_predicted.png'
        cv2.imwrite(img_mask_name, msm_marked)
        
        
def contour_func(nerve_mask,original_image,ids,nerve,shape):
    
    _, nerve_thresh_0 = cv2.threshold(nerve_mask, 175, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(image = nerve_thresh_0, mode = cv2.RETR_TREE, method = cv2.CHAIN_APPROX_SIMPLE)
    
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    """c = max(contours, key = cv2.contourArea)
    largestCnt = []
    for cnt in contours:
        if (len(cnt) > len(largestCnt)):
            largestCnt = cnt"""
    if len(contours[0]) != 0:
        
        M = cv2.moments(contours[0])
        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])
    contour_marked = cv2.putText(original_image, nerve, (x, y), cv2.FONT_HERSHEY_PLAIN, 1, 255)
    contour_marked = cv2.drawContours(original_image, [contours[0]], contourIdx = -1, 
                         color = (0, 255, 0), thickness = 2)
    
    return contour_marked


def predict():
    to_predict, ids = read_images(image_path='./images/test/')
    asm_masks = predict_masks(images_npy=to_predict,model=unet_model, h5_path='h5_files/unet-tgs-weights_100original_asm.h5')
    bp_masks = predict_masks(images_npy=to_predict,model=unet_model, h5_path='h5_files/unet-tgs-weights_100original_bp.h5')
    msm_masks = predict_masks(images_npy=to_predict,model=unet_model, h5_path='h5_files/unet-tgs-weights_100original_msm.h5')
    scm_masks = predict_masks(images_npy=to_predict,model=unet_model, h5_path='h5_files/unet-tgs-weights_100original_scm.h5')
    mask_to_image('asm',asm_masks,'./images/mask_predicted',ids)
    mask_to_image('bp',bp_masks,'./images/mask_predicted',ids)
    mask_to_image('msm',msm_masks,'./images/mask_predicted',ids)
    mask_to_image('scm',scm_masks,'./images/mask_predicted',ids)
    draw_contours('asm','./images/mask_predicted/','./images/test/','./images/predicted/',ids)