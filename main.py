# -*- coding: utf-8 -*-
from download_video import *
from launch_app_data import *
from train import *

# 각 label별로 2개씩 sample한다
max_samples = 2

"""# **데이터 다운로드**"""
#exclude if data already downloaded
download("train",max_samples)
download("test",max_samples)
download("val",max_samples)


# Load dataset in FiftyOne
#exclude if app not necessary
start_app_session()


"""## Training a PyTorchVideo classification model"""
import torch
if torch.cuda.is_available():
    DEVICE = torch.device('cuda')
else:
    DEVICE = torch.device('cpu')

print('Using PyTorch version:', torch.__version__, ' Device:', DEVICE)

train_model(DEVICE)