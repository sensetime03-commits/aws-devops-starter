# AWS + DevOps Starter Project

A small Flask API deployed to AWS with Terraform and a GitLab CI/CD pipeline.

```
Developer --git push--> GitLab CI --> test --> build image --> push to ECR --> update ECS service
                                                                                    |
Internet --> Application Load Balancer --> ECS Fargate task (Flask + gunicorn) --> CloudWatch Logs
```

## Folder structure

```
aws-devops-starter/
├── app/
│   ├── app.py               Flask API (/, /health, /notes)
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .dockerignore
│   └── tests/test_app.py
├── terraform/
│   ├── versions.tf          provider + optional S3 backend
│   ├── variables.tf
│   ├── network.tf           VPC, subnets, security groups
│   ├── ecr.tf               image registry
│   ├── alb.tf               load balancer + health check
│   ├── ecs.tf               cluster, task, service, IAM role, logs
│   ├── monitoring.tf        CloudWatch alarm
│   ├── outputs.tf
│   └── terraform.tfvars.example
├── .gitlab-ci.yml           CI/CD pipeline
└── .gitignore
```

## Phase 1: Run locally

```bash
cd app
pip install -r requirements.txt
pytest -v
python app.py                      # http://localhost:5000/health
# or with Docker:
docker build -t devops-starter .
docker run -p 5000:5000 devops-starter
```

## Phase 2: AWS setup

1. Do NOT use the root account. Create an IAM user (or use SSO) with permissions for EC2/VPC, ECS, ECR, ELB, IAM, CloudWatch.
2. Create a billing alarm (Billing > Budgets).
3. Install the AWS CLI and run `aws configure`.
4. Install Terraform (1.5+).

## Phase 3: Deploy the infrastructure

The ECS service needs an image in ECR, so create ECR first, push once, then create the rest.

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform apply -target=aws_ecr_repository.app

# push the first image
REPO=$(terraform output -raw ecr_repository_url)
REGION=us-east-1
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin ${REPO%%/*}
docker build -t $REPO:latest ../app
docker push $REPO:latest

# create everything else
terraform apply
terraform output app_url           # open in browser: /health, /notes
```

Test it:

```bash
curl http://<app_url>/health
curl -X POST http://<app_url>/notes -H "Content-Type: application/json" -d '{"text":"hello"}'
curl http://<app_url>/notes
```

Note: notes are stored in memory, so they reset when the container restarts. A good next step is to move them to DynamoDB or RDS.

## Phase 4: CI/CD with GitLab

1. Push this folder to a new GitLab project.
2. Add the CI/CD variables listed at the top of `.gitlab-ci.yml`.
   Get the names from `terraform output`.
3. Push a change to the main branch. The pipeline runs: test, build_and_push, deploy.

## Phase 5: Observability

- Logs: CloudWatch > Log groups > `/ecs/devops-starter`
- Alarm: `devops-starter-unhealthy-hosts` (add an SNS topic for email alerts)

## Clean up (important, avoids charges)

```bash
cd terraform
terraform destroy
```

## Cost notes

- The ALB costs about $16-20/month if left running. Fargate is small for 0.25 vCPU / 0.5 GB.
- Tasks run in public subnets to avoid the NAT gateway cost (~$32/month). For production, use private subnets + NAT.

## Next steps

- Remote state: create an S3 bucket + DynamoDB table and enable the backend in `versions.tf`
- Add `trivy image` and `tfsec` scans to the pipeline
- Add HTTPS with ACM + Route 53
- Split into dev and prod environments
- Replace GitLab access keys with OIDC role assumption
