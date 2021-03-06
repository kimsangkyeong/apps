# Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file
# except in compliance with the License. A copy of the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under the License.
#
# Content of revision : 
# - contents : Revised to upload/delete to S3 based on the contents of the input file (artefact)    
# - modifier : kimsangkyeong@gmail.com
"""
A BitBucket Builds template for deploying an application revision to AWS CodeDeploy
narshiva@amazon.com
v1.0.0
"""
from __future__ import print_function
import os
import sys
import argparse
import boto3
from botocore.exceptions import ClientError

def deploy_to_s3(bucket, artefact, bucket_key_prefix):
    try:
        changeinfo_list=[]
        fin = open(artefact,'rt')
        while True:
            line = fin.readline()
            if not line:
                break
            print(" line : {}".format(line))
            changeinfo_list.append(line)
        fin.close()
    except:
        print("Error in reading change info file. - ", artefact) 
        fin.close()
        return False

    # Create a low-level client with the service name 
    try:
        s3_client = boto3.client('s3')
    except ClientError as err:
        print("Failed to create boto3 client.\n" + str(err))
        return False

    # List of S3 handling exception files
    s3_except_list = ['changeinfo.list', '.gitignore', 'README.md',
                      'bitbucket-pipelines.yml']

    # upload / delete to s3
    tot_chg = len(changeinfo_list)
    for idx, changeinfo in enumerate(changeinfo_list):
        action  = changeinfo[:1]
        chgfile = changeinfo[2:-1] # trim space & carrage return
        #print("changeinfo : {}, action: {}, changefile: {}".format(changeinfo,action,chgfile))
        if chgfile in s3_except_list :
            print("({}/{}) S3 handling exception info : {}".format(idx+1, tot_chg, changeinfo))
            continue
        if action != 'D': # new, modified file
            print("({}/{}) s3 upload prepare : {} ".format(idx+1, tot_chg, chgfile))
            if bucket_key_prefix == "/" :
                bucket_key = chgfile
            else:
                if bucket_key_prefix[-1] == "/" :
                    bucket_key = bucket_key_prefix + chgfile
                else: 
                    bucket_key = bucket_key_prefix + '/' + chgfile
            if not upload_to_s3(s3_client, bucket, chgfile, bucket_key):
                return False
            print("({}/{}) s3 uploaded ".format(idx+1, tot_chg))
        else:             # deleted file
            print("({}/{}) s3 delete prepare : '{}' ".format(idx+1, tot_chg, chgfile))
    return True

def upload_to_s3(client, bucket, artefact, bucket_key):
    """
    Uploads an artefact to Amazon S3
    """
    try:
        print(" bucket_key : [ {} ] ".format(bucket_key));
        return True
        client.put_object(
            Body=open(artefact, 'rb'),
            Bucket=bucket,
            Key=bucket_key
        )
    except ClientError as err:
        print("Failed to upload artefact to S3.\n" + str(err))
        return False
    except IOError as err:
        print("Failed to access artefact in this directory.\n" + str(err))
        return False
    return True


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("bucket", help="Name of the existing S3 bucket")
    parser.add_argument("artefact", help="Name of the artefact to be uploaded to S3")
    parser.add_argument("bucket_key_prefix", help="Name of the S3 Bucket key prefix")
    args = parser.parse_args()

    if not deploy_to_s3(args.bucket, args.artefact, args.bucket_key_prefix):
        sys.exit(1)

if __name__ == "__main__":
    main()
