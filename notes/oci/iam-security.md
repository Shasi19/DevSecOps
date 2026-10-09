# OCI IAM and workload identity

## 1. Policy model

OCI IAM policies grant verbs on resource types to groups or dynamic groups in a scope, commonly a compartment or tenancy. Policies are human-readable and can inherit. A policy such as `Allow group PlatformAdmins to manage virtual-network-family in compartment Platform` is intentionally broad for a platform role; application teams should receive narrower permissions.

```text
Allow group AppOperators to read instance-family in compartment AppDev
Allow dynamic-group AppRuntime to read objects in compartment AppData
```

These examples require actual group/dynamic-group definitions and resource conditions. Validate exact syntax, matching rule, scope, and service-specific permissions in a sandbox. `manage` is broad; prefer the minimum verb/resource-family combination.

## 2. Human and workload principals

- Use identity federation, MFA, group-based access, and short-lived sessions for human operators.
- Dynamic groups match OCI resources by rules; overly broad matching gives every matching instance privileges.
- Instance principals let Compute instances call OCI APIs without embedding user API keys.
- Resource principals support supported managed services; verify service and policy prerequisites.
- CI should use a dedicated, narrowly scoped principal and isolated runner. Avoid copying an administrator API signing key into CI.

Test both intended access and denial to an unrelated compartment. Audit `CreatePolicy`, `UpdatePolicy`, group changes, key creation, and resource principal activity.

## 3. Secrets, keys, and cryptography

Use OCI Vault for managed encryption keys and secrets where appropriate. Grant secret read to the exact workload principal and vault/secret scope; rotate with a rollout procedure. Keep key-administrator and key-user roles distinct. Understand that KMS availability is a dependency for decrypt operations and that key deletion/scheduling has recovery consequences.

OCI service encryption at rest does not grant/deny access by itself. TLS, resource IAM, network path, application authorization, and secret lifecycle remain separate controls.

## 4. Guardrails and posture

Cloud Guard detects/responds to selected risky configurations and activity; tune detector/recipe targets and response actions to avoid unsafe automated remediation. Security Zones enforce constraints for resources in assigned zones—adopt them deliberately. Use vulnerability scanning and patch policy for Compute images, containers, and application dependencies.

## 5. Access-denied runbook

1. Capture request ID, timestamp, principal, operation, resource OCID, and region.
2. Verify the active CLI profile/instance principal and tenancy.
3. Check group membership or dynamic-group matching rule.
4. Trace policy statements, verb, resource type, compartment scope, and inheritance.
5. Check key/Vault policies, service-agent requirements, security-zone constraints, and quotas.
6. Inspect Audit events and retry with the narrowest justified grant.
7. Verify unrelated resources remain inaccessible.

Do not change a policy to `manage all-resources in tenancy` as a troubleshooting shortcut.

## Revision

Identity principal is not API key; dynamic-group membership is rule-based; policies grant but do not route traffic; Vault access has IAM and network prerequisites; key administration differs from key use; Cloud Guard detection is not prevention.
