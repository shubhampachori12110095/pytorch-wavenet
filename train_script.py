import time
import torch
import numpy as np
from torch.autograd import Variable
from wavenet_model import *
from audio_data import WavenetDataset
from wavenet_training import WavenetTrainer
from scipy.io import wavfile

# model = WaveNetModel(layers=6,
#                      blocks=4,
#                      dilation_channels=16,
#                      residual_channels=16,
#                      skip_channels=16,
#                      output_length=8)

model = load_latest_model_from('snapshots')
#model = torch.load('snapshots/snapshot_2017-12-10_09-48-19')

data = WavenetDataset(dataset_file='train_samples/clarinet/dataset.npz',
                      item_length=model.receptive_field + model.output_length - 1,
                      target_length=model.output_length,
                      file_location='train_samples/sapiens',
                      test_stride=200)

# torch.save(model, 'untrained_model')
print('the dataset has ' + str(len(data)) + ' items')
print('model: ', model)
print('receptive field: ', model.receptive_field)

optimizer = WavenetTrainer(model=model,
                           dataset=data,
                           lr=0.00001,
                           snapshot_path='snapshots',
                           snapshot_interval=500,
                           validate_interval=200)

print('start training...')
tic = time.time()
optimizer.train(batch_size=4,
                epochs=20)
toc = time.time()
print('Training took {} seconds.'.format(toc - tic))
