import time
import datetime
import sys
from datetime import datetime, timedelta, time
import argparse
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from phishpedia.phishpedia_config import load_config
from phishpedia.phishpedia_main import runit


if __name__ == '__main__':
    date = datetime.today().strftime('%Y-%m-%d')
    print('Today is:', date)
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', "--folder",
                        default='phishpedia/datasets/test_sites',
                        help='Input folder path to parse')
    parser.add_argument('-r', "--results", default=date + '_pedia.txt',
                        help='Input results file name')
    parser.add_argument('-c', "--config", default='phishpedia/configs/configs.yaml',
                        help='Input configuration file name')

    args = parser.parse_args()
    print(args)

    ELE_MODEL, SIAMESE_THRE, SIAMESE_MODEL, LOGO_FEATS, LOGO_FILES, DOMAIN_MAP_PATH = load_config(args.config)
    runit(args.folder, args.results, ELE_MODEL, SIAMESE_THRE, SIAMESE_MODEL, LOGO_FEATS, LOGO_FILES, DOMAIN_MAP_PATH)
    print('Process finish')
