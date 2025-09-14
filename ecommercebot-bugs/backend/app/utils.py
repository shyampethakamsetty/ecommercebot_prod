
import os, boto3, json
from botocore.exceptions import BotoCoreError, ClientError
def make_presigned_get_url(key, bucket=None, expires_in=3600):
    s3_bucket = bucket or os.getenv('ARTIFACTS_S3_BUCKET')
    if not s3_bucket or not key:
        return None
    try:
        s3 = boto3.client('s3',
                          aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                          region_name=os.getenv('AWS_REGION') )
        url = s3.generate_presigned_url('get_object', Params={'Bucket': s3_bucket, 'Key': key}, ExpiresIn=expires_in)
        return url
    except Exception:
        return None

# Redis streams publisher
import redis
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
def redis_stream_publish(task_id, payload):
    try:
        r = redis.from_url(REDIS_URL)
        stream = f"task_events:{task_id}"
        r.xadd(stream, {'data': json.dumps(payload)})
        return True
    except Exception:
        return False
