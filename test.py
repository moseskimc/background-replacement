from io import BytesIO
from PIL import Image

import requests
import os

from utils import format_single_double_quotes


if __name__ == "__main__":

    image_dir = "images"

    background_file_name = "background.jpg"
    background_file_path = os.path.join(
        image_dir,
        background_file_name
    )
    background_category = "background"

    # input image to extract salient object from
    input_image_file_name = "cat.jpg"
    input_image_file_path = os.path.join(
        image_dir,
        input_image_file_name
    )
    input_image_category = "cat"

    # read in files
    bg_image = open(
        background_file_path,
        'rb'
    )
    input_image = open(
        input_image_file_path,
        'rb'
    )

    # define post request params
    url = "http://0.0.0.0:9000/replace_background/"
    files = [
        ("files",  bg_image),
        ("files", input_image)
    ]

    metadata_dict = {
        "bg": {"filename": background_file_name, "category": background_category},
        "input": {"filename": input_image_file_name, "category": input_image_category}
    }
    metadata = [
        str(metadata_dict[key]) for key, _ in metadata_dict.items()
    ]
    metadata = [format_single_double_quotes(item) for item in metadata]

    # metadata = ['{"filename": "background.jpg", "category": "background"}',
    #             '{"filename": "cat.jpg", "category": "cat"}']

    data = {"data": metadata}

    # send POST request
    resp = requests.post(url=url, data=data, files=files)

    # read result image
    img = Image.open(BytesIO(resp.content))

    image_name = input_image_file_name.split(".")[0]
    bg_name = background_file_name.split(".")[0]

    save_dir = "images"
    filename = f"{image_name}_{bg_name}.png"
    filepath = os.path.join(
        save_dir,
        filename
    )
    img.save(filepath)
