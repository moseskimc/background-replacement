# background-replacement

This repo is a quick tutorial on how to replace the background of an image using a segmentation model and OpenCV.


## Deployment

Using Docker and FastAPI, we deploy a background replacement service on top of a pre-trained segmentation torch model called `FCN_ResNet50` and OpenCV.


### Docker

If you are using Apple Silicon please run the following command:

    export DOCKER_DEFAULT_PLATFORM=linux/amd64


To build the image, run:

    docker build -t bg-rep .

Finally, run the docker container via the command:

    docker run -d -p 9000:9000 bg-rep


## Test

You can find all sample images in `images/`. 

### Sample

The foreground of `cat.jpg` is the running cat. We replace the background of `cat.jpg` with `background.jpg` by cropping the center region.

#### Foreground

<img src="images/cat.jpg">

#### Background

<img src="images/background.jpg">


### Script

To run background replacement on `cat.jpg` simply run `test.py` from the project root.

```
python test.py
```

### Results

|![](images/cat.jpg)<br>Before|![](images/cat_background.png)<br>After|
|:-:|:-:|
