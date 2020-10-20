import json
import boto3
import botocore
import PIL
import io
import os
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from io import BytesIO

aws_region = "us-west-2"

font = ImageFont.truetype("arial.ttf", 50)

image_name = "KakaoTalk_20200715_142734079.jpg"
save_name = "KakaoTalk_20200715_142734079"
save_path = "D:\\mzc_project\\inference"
image_path = os.path.join("D:\\mzc_project\\Image\\siteTwo", image_name)
# source_img = Image.open(image_path)


# s3 = boto3.client("s3")
# bucket = "mgt-customlabels-resize-lambda"
# prefix = "resized_image_test/image-test-data/" + foldername

endpoint = "ObjectDetection-2020-10-20"
runtime = boto3.Session().client("sagemaker-runtime")

# SageMaker Endpoint 호출하여 추론 진행
with open(image_path, "rb") as f:
    payload = f.read()
response = runtime.invoke_endpoint(
    EndpointName=endpoint, ContentType="application/x-image", Body=payload
)

result = json.loads(response["Body"].read().decode())
print(result)  # Label 번호, 신뢰도, 좌표

# 추론결과(위의 result) json 파일로 저장
with open(os.path.join(save_path, save_name + ".json"), "w") as json_file:
    json.dump(result, json_file)

# 이미지 Boxing
for label in result:
    draw = ImageDraw.Draw(Image.open(image_path))

    x = int(label["prediction"] * Image.open(image_path).size[2])
    y = int(label["prediction"] * Image.open(image_path).size[3])
    x_right = int(x + label["prediction"] * Image.open(image_path).size[4])
    y_right = int(y + label["prediction"] * Image.open(image_path).size[5])

    draw.rectangle(((x, y), (x_right, y_right)), outline="red", width=5)
    draw.text((x, int(y + (y_right - y) / 3)), labels["Name"], font=font)

source_img.save(os.path.join(save_path, save_name), "JPEG")
