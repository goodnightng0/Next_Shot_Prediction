import pytorch_lightning
from transform import *
from combined import *

"""**Train**"""
def train_model(DEVICE):
  classification_module = VideoClassificationLightningModule().to(DEVICE)
  data_module = KineticsDataModule()
  trainer = pytorch_lightning.Trainer(gpus=1)
  trainer.fit(classification_module, data_module.train_dataloader(),data_module.val_dataloader())