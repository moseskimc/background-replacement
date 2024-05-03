# background-replacement

This repo implements a simple deployment of a FastAPI application to change the background of an input image. This background replacement is accomplished by using a ResNet based FCN model followed by image processing operations including background removal and image superimposition.

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

To run background replacement on `cat.jpg` simply run `test.py` from the project root.

```
python test.py
```

### Results

|![](images/cat.jpg)<br>Before|![](images/cat_background.png)<br>After|
|:-:|:-:|
