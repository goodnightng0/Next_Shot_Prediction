"""**Model**"""
from typing import Callable, List, Optional, Tuple, Union

import torch
import torch.nn as nn
import pytorchvideo
from pytorchvideo.layers.utils import set_attributes
from pytorchvideo.models.head import create_res_basic_head, create_res_roi_pooling_head
from pytorchvideo.models.net import MultiPathWayWithFuse, Net, DetectionBBoxNetwork
from pytorchvideo.models.resnet import create_bottleneck_block, create_res_stage
from pytorchvideo.models.stem import create_res_basic_stem
from pytorchvideo.models.x3d import create_x3d


def make_x3d():
  return pytorchvideo.models.x3d.create_x3d(
      input_channel=3, 
      model_num_class=10,
      norm=nn.BatchNorm3d,
      activation=nn.ReLU,
  )