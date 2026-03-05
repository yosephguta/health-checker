output "alb_dns_name" {
  description = "ALB DNS name (use this as the base URL to reach the app)"
  value       = module.ecs.alb_dns_name
}