import argparse
import os
import sys
import time

import numpy as np
import torch
from torch.autograd import Variable
from torch.optim import Adam
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision import transforms

import utils
from transformer_net import TransformerNet
from vgg import Vgg16

class StylizeImage(object):
    def __init__(self,style_image,content_image,model,scale,output,cuda=False):
        self.style_image = style_image
        self.content_image = content_image
        self.model = model
        self.content_scale = scale
        self.cuda = cuda
        self.output_image = output

    def stylize(self):
        content_image = utils.load_image(self.content_image, scale=self.content_scale)
        content_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Lambda(lambda x: x.mul(255))
        ])
        content_image = content_transform(content_image)
        content_image = content_image.unsqueeze(0)
        if self.cuda:
            content_image = content_image.cuda()
        content_image = Variable(content_image, volatile=True)

        style_model = TransformerNet()
        style_model.load_state_dict(torch.load(self.model))

        if self.cuda:
            style_model.cuda()
        output = style_model(content_image)

        if self.cuda:
            output = output.cpu()
        output_data = output.data[0]
        utils.save_image(self.output_image, output_data)

