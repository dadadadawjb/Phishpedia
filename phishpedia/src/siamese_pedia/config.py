import os
import subprocess
from tqdm import tqdm
from collections import OrderedDict
import numpy as np
import torch

from .siamese_retrain.bit_pytorch.models import KNOWN_MODELS
from .inference import pred_siamese


def config_siamese(num_classes:int, weights_path:str, targetlist_zip_path:str, grayscale=False):
    '''
    Load siamese configurations
    :param num_classes: number of protected brands
    :param weights_path: siamese weights
    :param targetlist_zip_path: targetlist zip path
    :param grayscale: convert logo to grayscale or not, default is RGB
    :return model: siamese model
    :return logo_feat_list: targetlist embeddings
    :return file_name_list: targetlist paths
    '''

    # Prepare data
    targetlist_dir = os.path.dirname(targetlist_zip_path)
    zip_file_name = os.path.basename(targetlist_zip_path)
    targetlist_folder = zip_file_name.split('.zip')[0]
    targetlist_path = os.path.join(targetlist_dir, targetlist_folder)

    if targetlist_zip_path.endswith('.zip') and not os.path.isdir(targetlist_path):
        os.makedirs(targetlist_path, exist_ok=True)
        subprocess.run(f'unzip -o "{targetlist_zip_path}" -d "{targetlist_path}"', shell=True)
    
    # Initialize model
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = KNOWN_MODELS["BiT-M-R50x1"](head_size=num_classes, zero_head=True)

    # Load weights
    weights = torch.load(weights_path, map_location='cpu')
    weights = weights['model'] if 'model' in weights.keys() else weights
    new_state_dict = OrderedDict()
    for k, v in weights.items():
        name = k.split('module.')[1]
        new_state_dict[name]=v
        
    model.load_state_dict(new_state_dict)
    model.to(device)
    model.eval()

    # Prediction for targetlists
    logo_feat_list = []
    file_name_list = []
    for target in tqdm(os.listdir(targetlist_path)):
        if target.startswith('.'): # skip hidden files
            continue
        for logo_path in os.listdir(os.path.join(targetlist_path, target)):
            if logo_path.endswith('.png') or logo_path.endswith('.jpeg') or logo_path.endswith('.jpg') or logo_path.endswith('.PNG') \
                                          or logo_path.endswith('.JPG') or logo_path.endswith('.JPEG'):
                if logo_path.startswith('loginpage') or logo_path.startswith('homepage'): # skip homepage/loginpage
                    continue
                logo_feat_list.append(pred_siamese(img=os.path.join(targetlist_path, target, logo_path), 
                                                   model=model, grayscale=grayscale))
                file_name_list.append(str(os.path.join(targetlist_path, target, logo_path)))
        
    return model, np.asarray(logo_feat_list), np.asarray(file_name_list)
