# -*- coding: utf-8 -*-
from googleapiclient import discovery
import os
import json
import base64

# Feature Type            Description
# FACE_DETECTION          顔認識
# LANDMARK_DETECTION      ランドマークの認識
# LOGO_DETECTION          製品ロゴの認識
# LABEL_DETECTION         画像コンテンツの認識 (ラベリング)
# TEXT_DETECTION          画像内テキストの認識 (OCR)
# SAFE_SEARCH_DETECTION   セーフサーチの判定
# IMAGE_PROPERTIES        最も有力な色を判定

DISCOVERY_URL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'

with open(os.path.join(os.path.dirname(__file__), 'api_key.json'), "r") as f:
    KEY = json.load(f)["api_key"]


def __get_vision_service():
    return discovery.build('vision', 'v1', developerKey=KEY,
                           discoveryServiceUrl=DISCOVERY_URL)

vision_api = __get_vision_service()


def ocr(img_base64_encoded="", test=False):
    if test:
        with open("test.png", "rb") as img_file:
            # https://github.com/GoogleCloudPlatform/cloud-vision/issues/55
            # https://github.com/GoogleCloudPlatform/cloud-vision/pull/58
            # img_base64_encoded = base64.b64encode(img_file.read())
            img_base64_encoded = base64.b64encode(img_file.read()).decode("utf-8")
    batch_request = [
        {
            "image": {
                "content": img_base64_encoded,
            },
            "features": [
                {
                    "type": "TEXT_DETECTION",
                }
            ]
        }
    ]

    request = vision_api.images().annotate(body={
        "requests": batch_request,
    })
    response = request.execute()
    if 'textAnnotations' in response["responses"][0]:
        return response["responses"][0]["textAnnotations"][0].get("description", None)
    else:
        return "取得に失敗しました"

if __name__ == '__main__':
    import unittest

    class TestApi(unittest.TestCase):
        def test_google_img(self):
            res = ocr(test=True)
            self.assertEqual(res, "Google\n")
    unittest.main()
