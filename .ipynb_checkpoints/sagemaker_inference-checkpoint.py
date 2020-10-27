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

s3 = boto3.client("s3")
bucket = "mgt-hnjng"
prefix = "mzc_project/test-image/20200715_131414.jpg"

endpoint = "ObjectDetection-2020-10-21"
runtime = boto3.Session().client("sagemaker-runtime")

source_img = s3.get_object(Bucket=bucket, Key=prefix)["Body"].read()
# print(source_img)
# inference_image = Image.open(io.BytesIO(source_img))

with open(source_img, "rb") as f:
    payload = f.read()
response = runtime.invoke_endpoint(
    EndpointName=endpoint, ContentType="application/x-image", Body=payload
)

result = json.loads(response["Body"].read().decode())
print(result)  # Label 번호, 신뢰도, 좌표

# # SageMaker Endpoint 호출하여 추론 진행
# with open(image_path, "rb") as f:
#     payload = f.read()
# response = runtime.invoke_endpoint(
#     EndpointName=endpoint, ContentType="application/x-image", Body=payload
# )

# result = json.loads(response["Body"].read().decode())
# print(result)  # Label 번호, 신뢰도, 좌표

# # 추론결과(위의 result) json 파일로 저장
# with open(os.path.join(save_path, save_name + ".json"), "w") as json_file:
#     json.dump(result, json_file)
# source_img = Image.open(image_path)
# # 이미지 Boxing
# for label in result["prediction"]:
#     draw = ImageDraw.Draw(source_img)

#     x_min = int(label[2] * source_img.size[0])
#     y_min = int(label[3] * source_img.size[1])
#     x_max = int(label[4] * source_img.size[0])
#     y_max = int(label[5] * source_img.size[1])

#     print(x_min)
#     print(y_min)
#     print(x_max)
#     print(y_max)

#     draw.rectangle(((x_min, y_min), (x_max, y_max)), outline="red", width=5)
#     draw.text((x_min, int(y_min + (y_max - y_min) / 3)), str(label[0]), font=font)
#     print(label[0])

# source_img.save(os.path.join(save_path, save_name + ".jpg"), "JPEG")
