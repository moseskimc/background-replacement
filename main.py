import json

from io import BytesIO

from fastapi import FastAPI, UploadFile, Response, File
from PIL import Image
from torchvision.models.segmentation import FCN_ResNet50_Weights, fcn_resnet50

from pydantic import BaseModel, model_validator
from typing import List, Optional

from utils import remove_background, superimpose, image_to_byte_array


# define metadata class
class ImageMetadata(BaseModel):
    filename: str
    category: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


# get model weights
weights = FCN_ResNet50_Weights.DEFAULT
# define transform so input dimensions are kept
transforms = weights.transforms(resize_size=None)

model = fcn_resnet50(weights=weights)
model.eval()


app = FastAPI()


@app.post("/replace_background/")
async def replace_background_endpoint(
    data: List[ImageMetadata],
    files: List[UploadFile] = File(...)
):

    bg_file, input_file = files
    # read in input image
    input_file_content = await input_file.read()
    input_image_pil = Image.open(BytesIO(input_file_content))
    # read in background image
    bg_file_content = await bg_file.read()
    bg_image_pil = Image.open(BytesIO(bg_file_content))
    # get image category
    _, image_metadata = data
    image_category = image_metadata.category
    foreground, _ = remove_background(
        model,
        weights,
        input_image_pil,
        transforms,
        image_category
    )

    new_bg_image = superimpose(bg_image_pil, foreground)

    # turn into bytes
    result = image_to_byte_array(new_bg_image)

    return Response(
        content=result,
        media_type="image/png"
    )
