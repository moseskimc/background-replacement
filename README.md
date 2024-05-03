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

`cat.jpg` is the foreground image whose background we replace with `background.jpg`.


|![](images/cat.jpg)<br>Foreground|![](images/background.jpg)<br>Background|
|:-:|:-:|

### Results

In order to run a background removal on the image `cat.jpg`, run:

    python test.py



<img src="images/cat_background.png">
