resource "aws_s3_bucket" "data_bucket" {
  bucket = "my-company-data-bucket"
  acl    = "public-read"
}

resource "aws_s3_bucket" "logs_bucket" {
  bucket = "my-company-logs"
}

# No versioning, no encryption, no lifecycle rules, public ACL
