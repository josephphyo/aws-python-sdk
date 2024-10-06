import boto3

s3 = boto3.resource("s3")
bucket_name = "joseph-boto-crud-123435"

# --- check bucket are already exist or not.
# --- If not exist, Create bucket.

all_buckets = [bucket.name for bucket in s3.buckets.all()]

if bucket_name not in all_buckets:
    print(f"{bucket_name} are not exist. Creating Now ....")
    s3.create_bucket(Bucket=bucket_name)
    print(f"{bucket_name} has been created")
else:
    print(f"{bucket_name} are already existed")

# --- create file and upload to S3 bucket.

file_1 = "file1.txt"
s3.Bucket(bucket_name).upload_file(Filename=file_1, Key=file_1)

# --- READ the Object inside the bucket - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/object/index.html

obj = s3.Object(bucket_name=bucket_name, key=file_1)
body = obj.get()["Body"].read()
print(body)

# --- DELETE the Object(File).

s3.Object(bucket_name=bucket_name, key=file_1).delete()

# --- DELETE the Bucket. Bucket must be Empty

bucket = s3.Bucket(bucket_name)
bucket.delete()

print(f"{bucket_name} is deleted!")
