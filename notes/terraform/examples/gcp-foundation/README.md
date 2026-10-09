# GCP foundation plan-only example

This example creates managed cloud resources if applied. It requires an existing project, billing, Compute API, and least-privilege permissions. Review the plan and cost before any apply. Use sandbox only.

```bash
cp terraform.tfvars.example terraform.tfvars
terraform fmt -check
terraform init
terraform validate
terraform plan -out=tfplan
terraform show tfplan
```

Do not commit `terraform.tfvars`, state, or saved plan files; they may contain sensitive values. The sample has no remote backend and is not production state management. For production, use a protected remote backend and keyless CI federation.
