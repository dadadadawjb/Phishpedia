# Global configuration
import os
import yaml

from .src.detectron2_pedia.config import config_detectron2
from .src.siamese_pedia.config import config_siamese


def load_config(cfg_path:str):

    # load config
    with open(cfg_path) as file:
        configs = yaml.load(file, Loader=yaml.FullLoader)

    # config detectron2
    ELE_CFG_PATH = configs['ELE_MODEL']['CFG_PATH'].replace('/', os.sep)
    ELE_CFG_PATH = os.path.abspath(ELE_CFG_PATH)
    ELE_WEIGHTS_PATH = configs['ELE_MODEL']['WEIGHTS_PATH'].replace('/', os.sep)
    ELE_WEIGHTS_PATH = os.path.abspath(ELE_WEIGHTS_PATH)
    ELE_CONFIG_THRE = configs['ELE_MODEL']['DETECT_THRE']
    ELE_MODEL = config_detectron2(ELE_CFG_PATH, ELE_WEIGHTS_PATH, conf_threshold=ELE_CONFIG_THRE)

    # config siamese
    SIAMESE_THRE = configs['SIAMESE_MODEL']['MATCH_THRE']
    DOMAIN_MAP_PATH = configs['SIAMESE_MODEL']['DOMAIN_MAP_PATH'].replace('/', os.sep)
    DOMAIN_MAP_PATH = os.path.abspath(DOMAIN_MAP_PATH)
    print('Load protected logo list')
    siamese_weights_path = configs['SIAMESE_MODEL']['WEIGHTS_PATH'].replace('/', os.sep)
    siamese_weights_path = os.path.abspath(siamese_weights_path)
    targetlist_zip_path = configs['SIAMESE_MODEL']['TARGETLIST_PATH'].replace('/', os.sep)
    targetlist_zip_path = os.path.abspath(targetlist_zip_path)
    SIAMESE_MODEL, LOGO_FEATS, LOGO_FILES = config_siamese(
                                                num_classes=configs['SIAMESE_MODEL']['NUM_CLASSES'],
                                                weights_path=siamese_weights_path,
                                                targetlist_zip_path=targetlist_zip_path)
    print('Finish loading protected logo list')

    return ELE_MODEL, SIAMESE_THRE, SIAMESE_MODEL, LOGO_FEATS, LOGO_FILES, DOMAIN_MAP_PATH
