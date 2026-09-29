resource "aws_ecr_repository" "app" {
  name         = var.project_name
  force_delete = true # lets 'terraform destroy' remove the repo even if it has images

  image_scanning_configuration {
    scan_on_push = true
  }
}

# Keep only the last 10 images to save storage cost
resource "aws_ecr_lifecycle_policy" "app" {
  repository = aws_ecr_repository.app.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep last 10 images"
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = 10
      }
      action = { type = "expire" }
    }]
  })
}
