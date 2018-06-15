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
    job_name = "".join([bucket_name, filename, "3"])
    job_uri = "https://s3.amazonaws.com/%s/%s" % (bucket_name, filename)
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='wav',
        LanguageCode='en-US',
        Settings={
            "ShowSpeakerLabels": True,
            "MaxSpeakerLabels": 2
        }
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
    return response

def parse_data(data):
    data = data.read()
    t_json = json.loads(data)

    items = t_json["results"]["items"]
    output = [item["alternatives"][0]["content"] for item in items]
    print(" ".join(output))

def get():
    url = "https://s3.amazonaws.com/aws-transcribe-us-east-1-prod/969144742973/speech-audio2output.wav2/asrOutput.json?X-Amz-Security-Token=FQoDYXdzEGwaDFDLyPGxc4H9LK7kWiK3A0dtYHzvgUJXb%2Bcwx2fL85pVfKdS7Z5TrLKZ9IslwJ%2BWR3LlL1J%2BiFUkJKRPlKzW9ebCMGLy%2Fb8pl79EKCNswN3MHbEIbgcLQ7fb33Tq%2BYYME0WnQruaTUoW1zS72z31Myv0TupOTNlyZVdcjZjKE9SAWc7ArLfWmGeqgARD6tZwqO8v%2FnBLB5bmKZFRdjBeogIKtYIfB0fPEaviAuauJn43HFYVzSxAbxQc0%2BM1GwjPRG1qk64WJJgnZkiG3HWmnw21xfcm9k6AwntroonZKp1gywuY93omuyXH2th6H8DBa%2BCVbAG%2BwExrUoC3va18Vj9htN4XWTBP8jBtM0WdfIJ9DdhxNqGWHLHofeTPCaKkN1AAX38w85Ab35hYsKqwMOFU6j0bzSGlEsSrsOi%2BFgNuulY0hnECFRvHm2rDXg5Y0wSZ4Ed7gT4mHsXuQXYBeE2kXPnVxBlLkVQU%2Fo%2F4OEI%2FPh9LRbKqXzrbQm%2Btmna6xaKEW1eoiAekVqBpyyJWyam6kfkK1QxQuBABiQ8Y2OBFqktQAv%2Bu6TfxDPIGTWGcjc%2BP5cQUjfEZPI6O8MOux2D1gBxuBzQouK6H2QU%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20180614T034945Z&X-Amz-SignedHeaders=host&X-Amz-Expires=899&X-Amz-Credential=ASIAJDWO5NRDOMLWERCA%2F20180614%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=de39060c69e0bb4b6da8900594a353463f43a4ae66756e5e8c58763cdf9d0191"
    response = urllib.request.urlopen(url)
    return response

upload_s3("speech-audio2", "output2.wav")
data = transcribe("speech-audio2", "output2.wav")
# data = get()
parse_data(data)