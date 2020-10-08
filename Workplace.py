import json
import boto3
import cv2
import math
import io
def analyzeVideo():
    videoFile = "C:\\Users\\HP\\Downloads\\Crowd in a mall.mp4"
    projectVersionArn = "arn:aws:rekognition:us-east-1:115025340805:project/WorkplaceSafetyNew/version/WorkplaceSafetyNew.2020-10-06T18.55.34/1601990734982"
    rekognition = boto3.client('rekognition',
                           aws_access_key_id="ASIARVSALNGCWUMELSZW",
                           aws_secret_access_key="pRUSwCT0Z0K6dkkq2HxpNwHGsGXQWpI0DFkssxsB",
     aws_session_token="FwoGZXIvYXdzEP///////////wEaDJpezaC6jCpHK+LWxiLFAUHnA7w9gRLhf7gMfDyUhKCLXtAVm8+kncg5jrZSY4B2eD/o5MXQvElcZh7Od1eYu1sektTOAHzuziMWj1refll5wkmBXT55nmK2Pj4ZR3wtsRnvM6jg6mweEqc3ZXGxGleCrE9/JClbQmMuJW/r+ARAWkqw3z8wdTylmqN3Sum1USsXI4oKMRHZjd16SKwUO34RNvn4XxyxFy2BI2xXWbVLRn6+E0cVfrKRCDpL8+Kz6WYYmvnk5+GIj8saOwYh4U0bkeM+KNbG+vsFMi2bTPPDjVTXGL477HZ1GMyILXnQCV61v8hpyhE8ALvxoNQiBdMLCZcz4eQWqvo=",
                           region_name='us-east-1')
    customLabels = []
    cap = cv2.VideoCapture(videoFile)
    frameRate = cap.get(5) #frame rate
    while(cap.isOpened()):
        frameId = cap.get(1) #current frame number
        print("Processing frame id: {}".format(frameId))
        ret, frame = cap.read()
        if (ret != True):
            break
        if (frameId % math.floor(frameRate) == 0):
            hasFrame, imageBytes = cv2.imencode(".jpg", frame)
            if(hasFrame):
                response = rekognition.detect_custom_labels(
                    Image={
                        'Bytes': imageBytes.tobytes(),
                    },
                    ProjectVersionArn = projectVersionArn
                )

        for elabel in response["CustomLabels"]:
            elabel["Timestamp"] = (frameId/frameRate)*1000
            customLabels.append(elabel)

    for i in customLabels:
        print(i)
        print('\n')
    with open(videoFile + ".json", "w") as f:
        f.write(json.dumps(customLabels))
    cap.release()
analyzeVideo()
