# background-replacement

This repo implements a simple deployment of a FastAPI application that replaces the background of an image. Background replacement is accomplished by creating a segmentation mask of the image foreground using a ResNet-based FCN model followed by background removal and image superimposition.

## Docker

If running on Apple silicon please export the following variable in your terminal before building your Docker image.

    export DOCKER_DEFAULT_PLATFORM=linux/amd64


1. Build the image
```bash
    docker build -t bg-rep .
```

2. Run the container
```bash
    docker run -d -p 9000:9000 bg-rep
```



## Test

You can find all sample images in `images/`. 

### Sample

The foreground of `cat.jpg` is the running cat. We replace the background of `cat.jpg` with `background.jpg` by cropping the center region.

#### Foreground

<img src="images/cat.jpg">

#### Background

<img src="images/background.jpg">


### Script

To replace the background of `cat.jpg` with `background.jpg`, run the script `test.py` from the project root directory.

```shell
python test.py
```

The following code block encapsulates the main function of the script `test.py`, which is to send image and json data as a POST request to the deployed FastAPI server running on Docker and receive a file buffer corresponding to the new image. The definition of variables `input_image`, `bg_file`, and `metadata` are omitted for brevity.

```python
import requests

from PIL import Image
from io import BytesIO

url = "http://0.0.0.0:9000/replace_background/"
files = [
    ("input_file", input_image),
    ("bg_file",  bg_image)
]

data = {"data": metadata}

resp = requests.post(url=url, data=data, files=files)
img = Image.open(BytesIO(resp.content))
```

|![](images/cat.jpg)<br>Before|![](images/cat_background.png)<br>After|
|:-:|:-:|
