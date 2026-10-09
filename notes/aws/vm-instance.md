# EC2 virtual machine: purpose, creation, use, and cleanup

## What an EC2 instance is for

An EC2 instance is a virtual server for workloads that need an operating system, custom agents, legacy software, specialized compute, or control below a managed runtime. Prefer Lambda, ECS/Fargate, App Runner, or another managed option when you do not need a VM; a VM creates patching, capacity, and host-security responsibilities.

Typical uses: a controlled jump/management host (prefer Systems Manager Session Manager), a stateless application node in an Auto Scaling group, a worker with a specialized image, or a temporary migration utility. Do not use a single long-lived VM as the only production copy of a critical service.

## Before creation

You need an authorized sandbox account/Region; a VPC and private subnet; a security group allowing only required inbound traffic; an instance profile with least-privilege application permissions and SSM access; an approved patched AMI; a keyless admin path; encrypted storage; tags/owner; budget and teardown plan. Check account quotas and AMI architecture compatibility.

Do not assign a public IP by default. For administration, use Systems Manager Session Manager or a controlled bastion. Never expose SSH to `0.0.0.0/0`.

## Create a private instance (instructional CLI)

Set explicit values from your approved environment. The AMI parameter shown is the Amazon Linux 2023 public SSM parameter; verify it resolves to a supported AMI in your Region before launching.

```bash
export AWS_PROFILE=dev-sandbox
export AWS_REGION=us-east-1
export SUBNET_ID=subnet-REPLACE
export SECURITY_GROUP_ID=sg-REPLACE
export INSTANCE_PROFILE=REPLACE-SSM-APP-INSTANCE-PROFILE
export AMI_ID="$(aws ssm get-parameter \
  --name /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 \
  --query Parameter.Value --output text)"

aws ec2 run-instances \
  --image-id "$AMI_ID" \
  --instance-type t3.small \
  --subnet-id "$SUBNET_ID" \
  --security-group-ids "$SECURITY_GROUP_ID" \
  --iam-instance-profile Name="$INSTANCE_PROFILE" \
  --metadata-options HttpTokens=required,HttpEndpoint=enabled \
  --block-device-mappings 'DeviceName=/dev/xvda,Ebs={VolumeSize=20,VolumeType=gp3,Encrypted=true,DeleteOnTermination=true}' \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=dev-lab-ec2},{Key=Environment,Value=dev},{Key=Owner,Value=REPLACE}]' \
  --count 1
```

This does not create the VPC, subnet, security group, or instance profile; verify them first. Check subnet auto-assign-public-IP settings and route table: a private subnet should not provide an unintended public route. Add `--dry-run` first to test authorization (AWS dry-run does not validate all launch-time dependencies).

## Use and verify

```bash
aws ec2 describe-instances --filters Name=tag:Name,Values=dev-lab-ec2 \
  --query 'Reservations[].Instances[].[InstanceId,State.Name,PrivateIpAddress,PublicIpAddress]' \
  --output table
aws ssm describe-instance-information --filters Key=InstanceIds,Values=i-REPLACE
aws ssm start-session --target i-REPLACE --region "$AWS_REGION"
```

Use Session Manager to administer without inbound SSH. Install only required software with a controlled package/image process; configure CloudWatch/SSM inventory/patching; attach application permissions to the instance role, not local static keys. Put replaceable app instances in a launch template and Auto Scaling group across AZs. Store durable state outside the VM.

Verify: instance has no public IP; IMDSv2 is required; root volume is encrypted; SSM reports online; host patch/monitoring is active; the attached role can perform only expected actions; service health is observed from an external synthetic/health check.

## Troubleshooting

- **SSM offline:** check instance profile SSM permissions, SSM agent/service, DNS and egress to required SSM endpoints, time sync, and VPC endpoint policy.
- **Cannot reach service:** inspect route table, security-group rules in both directions, NACL return traffic, DNS, process listener, and host firewall.
- **Instance fails launch:** check AMI/architecture, subnet IP capacity, quota, instance-type availability, KMS permissions, and exact EC2 event/error.
- **Unexpected public reachability:** inspect public IP, IGW route, security groups, NACLs, load balancer, and host firewall; remove exposure at source and investigate access logs.

## Stop, retain, and terminate

Stopping can preserve EBS but does not stop every attached charge; Elastic IPs, snapshots, and other resources may continue billing. Termination may delete the root volume according to its delete-on-termination setting. Snapshot/back up only approved state before teardown. Confirm instance ID and environment tags; terminate only the lab-owned instance and remove unused security groups, snapshots, IPs, and role permissions according to change control. Never terminate by broad tag selector without reviewing the matched IDs.
