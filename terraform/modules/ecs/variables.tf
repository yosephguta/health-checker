variable "environment" {
  type        = string
  description = "Environment name (staging or prod)"
}

variable "repository_url" {
  type        = string
  description = "ECR repository URL (no tag). Example: 123.dkr.ecr.us-east-1.amazonaws.com/health-checker"
}

variable "image_tag" {
  type        = string
  description = "Image tag to deploy"
  default     = "latest"
}

variable "vpc_id" {
  type        = string
  description = "VPC ID from networking module"
}

variable "public_subnet_ids" {
  type        = list(string)
  description = "Public subnet IDs (at least two for ALB)"
}

variable "alb_sg_id" {
  type        = string
  description = "Security group ID for the ALB"
}

variable "ecs_sg_id" {
  type        = string
  description = "Security group ID for ECS tasks"
}

variable "app_port" {
  type        = number
  description = "Container port the app listens on"
  default     = 8000
}

variable "cpu" {
  type        = number
  description = "Task CPU units (1024 = 1 vCPU)"
  default     = 256
}

variable "memory" {
  type        = number
  description = "Task memory in MiB"
  default     = 512
}

variable "desired_count" {
  type        = number
  description = "Number of tasks to run"
  default     = 1
}