from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor


def config_detectron2(cfg_path, weights_path, conf_threshold):
    '''
    Configure weights and confidence threshold
    :param cfg_path:
    :param weights_path:
    :param conf_threshold:
    :return:
    '''
    cfg = get_cfg()
    cfg.merge_from_file(cfg_path)
    cfg.MODEL.WEIGHTS = weights_path
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = conf_threshold
    # uncomment if you installed detectron2 cpu version
    # cfg.MODEL.DEVICE = 'cpu'

    # Initialize model
    predictor = DefaultPredictor(cfg)
    return predictor
