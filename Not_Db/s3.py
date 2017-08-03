import json
import boto3
import os
import requests
from botocore.exceptions import ClientError
from threading import Thread
from time import sleep

client = boto3.client('s3')
resource = boto3.resource('s3')
region = 'eu-west-1'
def pather(*args):
    return "/".join([arg for arg in args])

def init(path, name):
    print path
    if name == "favicon.ico":
        return None
    policy ={
                "Version":"2012-10-17",
                "Statement":[{
                    "Sid":"PublicReadGetObject",
                            "Effect":"Allow",
                      "Principal": "*",
                          "Action":["s3:GetObject"],
                          "Resource":["arn:aws:s3:::{}/*".format(name)
                    ]
                  }
                ]
              }
    try:
        client.create_bucket(
                ACL='public-read',
                Bucket=name,
                CreateBucketConfiguration={
                    'LocationConstraint': region 
                }
                )
        client.put_bucket_policy(
                Bucket=name,
                Policy=json.dumps(policy)
                )
        client.put_bucket_website(
                Bucket=name,
                WebsiteConfiguration={
                    'ErrorDocument': {
                        'Key': 'error.html'
                    },
                    'IndexDocument': {
                        'Suffix': 'index.html'
                    }
                }
                )
    except ClientError as e:
        return e
        

def write(key, value, path, name):
    with open(pather(path, key), 'w') as page:
        page.write(json.dumps(value))
    print key, path, name, key, {'ContentType': 'application/json'}
    client.upload_file(key, name, key, ExtraArgs={'ContentType': 'application/json'})
    os.remove(key)    
        
def _write(*args):
    t = Thread(target=thread_write, args=args)
    t.start()

def read(key, path, name):
    s3_path = "https://s3-{}.amazonaws.com/{}/{}".format(
            region,
            name,
            key
            )

    return requests.get(s3_path).json()
    

def remove(key, path, name):
    client.delete_object(
            Bucket=name,
            Key=key
            )


def _remove(*args):
    t = Thread(target=thread_remove, args=args)
    t.start()


def drop(path, name):
    bucket = resource.Bucket(name)
    bucket.object_versions.all().delete()
    bucket.delete()

