resource "aws_ecr_repository" "this" {
  name = var.repository_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_lifecycle_policy" "this" {
  repository = aws_ecr_repository.this.name

  policy = jsonencode({
    rules = [
      # 1) Expire untagged images older than 1 day
      {
        rulePriority = 1
        description  = "Expire untagged images older than 1 day"
        selection = {
          tagStatus   = "untagged"
          countType   = "sinceImagePushed"
          countUnit   = "days"
          countNumber = 1
        }
        action = {
          type = "expire"
        }
      },

      # 2) Keep only the last 10 tagged images
      # NOTE: ECR lifecycle policies require tagPrefixList when tagStatus = "tagged".
      # This uses a broad prefix of "" (empty string) to match tags by prefix.
      # If AWS rejects this in your account, replace with your real tag prefixes
      # (e.g., ["v", "release-", "prod-", "staging-"]).
      {
        rulePriority = 2
        description  = "Keep only the last 10 tagged images"
        selection = {
          tagStatus     = "any"
          countType     = "imageCountMoreThan"
          countNumber   = 10
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}