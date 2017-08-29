import json
import boto3
import os
import requests
import StringIO
from flask import send_file
from botocore.exceptions import ClientError
from threading import Thread
from time import sleep

client = boto3.client('s3')
resource = boto3.resource('s3')
region = 'eu-west-1'
def pather(*args):
    return "/".join([arg for arg in args])

def init(path, name):
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
        

def write(key, value, path, name, raw=False):
    page = StringIO.StringIO()
    if raw:
        page.write(value)
        extra_args={}
    else:    
       page.write(json.dumps(value))
       extra_args={'ContentType': 'application/json'}
    page.seek(0)
    client.upload_fileobj(page, name, key, ExtraArgs=extra_args)
        
def _write(*args):
    t = Thread(target=thread_write, args=args)
    t.start()

def read(key, path, name, raw=False):
    s3_path = "https://s3-{}.amazonaws.com/{}/{}".format(
            region,
            name,
            key
            )
    if raw:
        contents = StringIO.StringIO()
        contents.write(requests.get(s3_path).content)
        contents.seek(0)
        return send_file(contents, attachment_filename=key)
    else:
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

