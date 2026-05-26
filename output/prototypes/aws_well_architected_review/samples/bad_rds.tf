resource "aws_db_instance" "main" {
  allocated_storage    = 500
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.r5.2xlarge"
  db_name              = "production"
  username             = "admin"
  password             = "SuperSecret123!"
  publicly_accessible  = true
  skip_final_snapshot  = true
  multi_az             = false
  storage_encrypted    = false
  backup_retention_period = 0
}

# Hard-coded password, publicly accessible, no encryption, no backups, single-AZ
