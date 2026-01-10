import boto3

def authenticate_s3(aws_access_key_id, aws_secret_access_key, region_name):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )
    return s3_client

def list_s3_objects(s3_client, bucket_name, prefix=None):
    params = {'Bucket': bucket_name}
    if prefix:
        params['Prefix'] = prefix
    response = s3_client.list_objects_v2(**params)
    return response.get('Contents', [])