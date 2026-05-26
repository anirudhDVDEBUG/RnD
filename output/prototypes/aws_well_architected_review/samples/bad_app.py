import os
import boto3

# Hard-coded credentials
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DB_PASSWORD = "SuperSecret123!"

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

def get_data(bucket, key):
    return s3.get_object(Bucket=bucket, Key=key)

def store_user_data(user_input):
    # No input validation
    query = f"INSERT INTO users VALUES ('{user_input}')"
    return query
