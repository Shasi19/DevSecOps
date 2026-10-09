# AWS for DevOps

## Mental model

AWS is a collection of regional services. An account is the security and billing boundary; a Region contains independent service deployments; Availability Zones provide fault isolation within a Region. Design around failure of individual instances, zones, credentials, and deployments rather than assuming infrastructure is permanent.

## Core building blocks

- **Identity:** IAM users, roles, policies, and federation. Prefer short-lived role credentials and narrowly scoped permissions over long-lived access keys.
- **Networking:** VPCs, subnets, route tables, security groups, and network ACLs. Public/private placement and explicit egress paths are key design choices.
- **Compute and data:** EC2, ECS/EKS, Lambda, S3, RDS, and DynamoDB solve different workload and operational needs. Choose based on control, scaling, consistency, and operations—not fashion.
- **Operations:** CloudWatch metrics/logs/alarms, CloudTrail audit events, Systems Manager, and cost allocation tags.

## Delivery workflow

1. Establish organization/account guardrails, identity federation, logging, and budgets.
2. Define infrastructure as code; review plans and protect state/secrets.
3. Build immutable artifacts, scan them, and publish to controlled registries.
4. Deploy through staged environments with health checks, alarms, and rollback.
5. Test recovery, permissions, and cost assumptions continuously.

## Security and reliability

Use least privilege, encryption in transit and at rest, private networking where appropriate, and managed secret storage. Separate production access and deployment roles. Multi-AZ improves availability but does not replace backups or disaster-recovery tests. Define RTO/RPO, verify restore procedures, and monitor service quotas and spend.

## Practice

Build a private application tier behind a load balancer, store data in a managed database, and expose only required paths. Add role-based deployment, centralized logs, an availability alarm, and a tested backup restore. Explain the blast radius if one AZ or one credential is compromised.

## Further reading

[AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) · [IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
