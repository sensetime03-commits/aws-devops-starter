variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name prefix for all resources"
  type        = string
  default     = "devops-starter"
}

variable "container_port" {
  description = "Port the app listens on"
  type        = number
  default     = 5000
}

variable "desired_count" {
  description = "Number of running tasks"
  type        = number
  default     = 1
}

variable "image_tag" {
  description = "Docker image tag to deploy"
  type        = string
  default     = "latest"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}
