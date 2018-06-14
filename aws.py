from __future__ import print_function
import time
import boto3

transcribe = boto3.client('transcribe')
job_name = "test_through_cli3"
job_uri = "https://s3.amazonaws.com/speech-audio2/test2.m4a"
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