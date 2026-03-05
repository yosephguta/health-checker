terraform {
  backend "s3" {
    bucket         = "health-checker-tfstate-857790692126"
    key            = "health-checker/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "health-checker-tfstate-lock"
    encrypt        = true
  }
}