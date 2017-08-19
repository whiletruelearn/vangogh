import torch
import os
from PIL import Image
from torch.autograd import Variable

class Utils(object):

    @staticmethod
    def load_models(model_dir):
        model_files = [f for f in os.listdir(model_dir) if f.endswith("pth")]
        models = {f[:-4]: os.path.join(model_dir,f) for f in model_files}
        return models

    @staticmethod
    def load_image(filename, size=None, scale=None):

        img = Image.open(filename)
        wi,hi = img.size
        if wi > 600:
            img = img.resize((600, hi*600/wi),Image.ANTIALIAS)
	elif hi > 600:
	    img = img.resize((wi*600/hi,600),Image.ANTIALIAS)

        elif scale is not None:
            img = img.resize((int(img.size[0] / scale), int(img.size[1] / scale)), Image.ANTIALIAS)

        print "Image size is {}".format(img.size)
        return img

    @staticmethod
    def save_image(filename, data):
        img = data.clone().clamp(0, 255).numpy()
        img = img.transpose(1, 2, 0).astype("uint8")
        img = Image.fromarray(img)
        img.save(filename)

    @staticmethod
    def gram_matrix(y):
        (b, ch, h, w) = y.size()
        features = y.view(b, ch, w * h)
        features_t = features.transpose(1, 2)
        gram = features.bmm(features_t) / (ch * h * w)
        return gram

    @staticmethod
    def normalize_batch(batch):
        # normalize using imagenet mean and std
        mean = batch.data.new(batch.data.size())
        std = batch.data.new(batch.data.size())
        mean[:, 0, :, :] = 0.485
        mean[:, 1, :, :] = 0.456
        mean[:, 2, :, :] = 0.406
        std[:, 0, :, :] = 0.229
        std[:, 1, :, :] = 0.224
        std[:, 2, :, :] = 0.225
        batch = torch.div(batch, 255.0)
        batch -= Variable(mean)
        batch = batch / Variable(std)
        return batch
