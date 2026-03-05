terraform {
  backend "s3" {
    bucket         = "health-checker-tfstate-857790692126"
    key            = "health-checker/staging/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "health-checker-tfstate-lock"
    encrypt        = true
  }
}

provider "aws" {
  region = "us-east-1"
}

module "networking" {
  source      = "../../modules/networking"
  environment = "staging"
  vpc_cidr    = "10.0.0.0/16"
}

module "ecr" {
  source          = "../../modules/ecr"
  repository_name = "health-checker"
}

module "ecs" {
  source            = "../../modules/ecs"
  environment       = "staging"
  repository_url    = module.ecr.repository_url
  image_tag         = "latest"

  vpc_id            = module.networking.vpc_id
  public_subnet_ids  = module.networking.public_subnet_ids
  alb_sg_id          = module.networking.alb_sg_id
  ecs_sg_id          = module.networking.ecs_sg_id

  app_port      = 8000
  desired_count = 1
  cpu           = 256
  memory        = 512
}