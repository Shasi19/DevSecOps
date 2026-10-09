# GCP foundation plan-only example

This example creates managed cloud resources if applied. It demonstrates a real provider `for_each` subnet map and a real conditional `count` firewall rule. It requires an existing project, billing, Compute API, and least-privilege permissions. Review the plan and cost before any apply. Use sandbox only.

```bash
cp terraform.tfvars.example terraform.tfvars
terraform fmt -check
terraform init
terraform validate
terraform plan -out=tfplan
terraform show tfplan
```

Do not commit `terraform.tfvars`, state, or saved plan files; they may contain sensitive values. The sample has no remote backend and is not production state management. For production, use a protected remote backend and keyless CI federation.

Changing a subnet map key means Terraform sees one key removed and another added; inspect the plan for subnet replacement and dependent resources. Keep keys stable. The optional firewall rule only targets VMs tagged `web-backend`; it is not a complete load-balancer/security policy.
