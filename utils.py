import torch
import cv2
import numpy as np

from PIL import Image
from io import BytesIO
from torchvision.transforms.functional import pil_to_tensor
from torchvision.io.image import read_image


def image_to_byte_array(image: Image):
    # instantiate memory buffer
    imgByteArr = BytesIO()
    # assign image to buffer
    image.save(imgByteArr, format="PNG")
    # turn image buffer to bytes object
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


def format_single_double_quotes(item_str: str):
    # util function to format data parameter
    # when sending POST request
    new_item_str_list = []
    for ch in item_str:
        if ch == "'":
            new_item_str_list.append('"')
        elif ch == '"':
            new_item_str_list.append("'")
        else:
            new_item_str_list.append(ch)

    return ''.join(new_item_str_list)


def make_transparent_foreground(foreground, mask):

    # extract individual channels from pic
    b, g, r = cv2.split(np.array(foreground).astype('uint8'))
    # add an extra channel to create transparent background
    a = np.ones(mask.shape, dtype='uint8') * 255
    alpha_im = cv2.merge([b, g, r, a], 4)
    bg = np.zeros(alpha_im.shape)
    # concate mask along axis 2
    new_mask = np.stack([mask, mask, mask, mask], axis=2)
    # using mask copy foreground pixels on top of transparent background
    foreground = np.where(new_mask, alpha_im, bg).astype(np.uint8)

    return foreground


def get_class_indices(model_weights):
    # index to keep track of segmentation masks by class
    segmentation_classes = model_weights.meta["categories"]
    return {cls: idx for (idx, cls) in enumerate(segmentation_classes)}


def remove_background(model,
                      model_weights,
                      pil_image,
                      transforms,
                      category="cat"):

    # load images
    # input_image = Image.open(file_path)  # read in as numpy array
    img = pil_to_tensor(pil_image)  # convert to torch tensor

    # apply transfoormation to image
    batch = torch.stack([transforms(img)])

    # extract masks corresponding to classes
    prediction = model(batch)["out"]
    class_dim = 1
    normalized_masks = prediction.softmax(dim=1)

    # get mask corresponding to category
    class_to_idx = get_class_indices(model_weights)
    boolean_mask = (normalized_masks.argmax(class_dim) == class_to_idx[category])
    mask = boolean_mask.squeeze()

    # create empty background array for white/black mask
    background = np.zeros(mask.shape)
    bin_mask = np.where(mask, 255, background).astype(np.uint8)
    # extract foreground
    foreground = make_transparent_foreground(pil_image, bin_mask)

    return foreground, bin_mask


def superimpose(background, foreground):

    # background dimensions must be larger than foreground
    final_foreground = Image.fromarray(foreground)
    # background = Image.open(background_file)

    # let's center foreground inside background and crop    
    x = (background.size[0]-final_foreground.size[0])/2
    y = (background.size[1]-final_foreground.size[1])/2
    box = (x, y, final_foreground.size[0] + x, final_foreground.size[1] + y)
    # crop background to foreground dimensions
    crop = background.crop(box)
    final_image = crop.copy()
    # overlay the foreground image in the centre of the background
    paste_box = (0,
                 final_image.size[1] - final_foreground.size[1],
                 final_image.size[0],
                 final_image.size[1])
    final_image.paste(final_foreground, paste_box, mask=final_foreground)

    return final_image
