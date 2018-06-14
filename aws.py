from __future__ import print_function
import time
import boto3

def upload_s3(file):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket("speech-audio2")
    bucket.upload_file("sample1.m4a", "sample1.m4a")

def transcribe(uri):
    transcribe = boto3.client('transcribe')
    job_name = "test_through_cli3"
    job_uri = "https://s3.amazonaws.com/speech-audio2/sample1.m4a"
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

with open("sample1.m4a") as f:
    upload_s3(f)