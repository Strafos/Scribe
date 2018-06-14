from __future__ import print_function
import urllib.request
import time
import json

import boto3

def upload_s3(bucket_name, filename):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    response = bucket.upload_file(filename, filename)
    print(response)

def transcribe(bucket_name, filename):
    transcribe = boto3.client('transcribe')
    job_name = "".join([bucket_name, filename, "2"])
    job_uri = "https://s3.amazonaws.com/%s/%s" % (bucket_name, filename)
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp4',
        LanguageCode='en-US'
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("wait")
        time.sleep(5)
    print(status)
    trans_url = status["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    response = urllib.request.urlopen(trans_url)
    return data

def parse_data(data)
    data = data.read()
    t_json = json.loads(data)

    items = t_json["results"]["items"]
    output = [item["alternatives"][0]["content"] for item in items]
    print(output)

with open("sample1.m4a") as f:
    upload_s3("speech-audio2", "sample1.m4a")
transcribe("speech-audio2", "sample1.m4a")