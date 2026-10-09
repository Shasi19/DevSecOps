# Kubernetes workload deployment lifecycle

## 1. Confirm cluster and ownership

Verify the current context, cluster, namespace owner, API version, CNI/network-policy support, admission controls, quota, storage class, ingress controller, and maintenance window:

```bash
kubectl config current-context
kubectl cluster-info
kubectl get nodes -o wide
kubectl get namespace
```

Do not run production changes against a context selected implicitly. Use a dedicated deployment identity with namespace-scoped RBAC, not cluster-admin from a laptop.

## 2. Prepare workload

Build and scan an immutable image; identify digest and provenance. Define Deployment (or appropriate workload), Service, resource requests/limits, readiness/startup/liveness probes, non-root security context, service account, ConfigMap/secret integration, topology spread, disruption budget, network policy, and autoscaling. Keep credentials out of manifests/source.

## 3. Validate and deploy

```bash
kubectl apply --dry-run=server -f manifests/
kubectl diff -f manifests/
kubectl apply -f manifests/
kubectl rollout status deployment/my-service -n my-namespace --timeout=5m
kubectl get pods,svc,endpoints -n my-namespace
```

Use reviewed GitOps/CI for production. Server-side dry-run/diff help but are not a complete security review. Verify image digest and policy/admission result.

## 4. Verify user path

Check Pod readiness, Service endpoints, DNS, ingress/Gateway route, TLS, network policy, dependency access, application logs, and external synthetic/SLI. Confirm the rollout does not violate error/latency budgets. Observe at least the agreed bake period before promotion.

## 5. Troubleshoot and rollback

Use events, `describe`, current/previous container logs, rollout history, node conditions, quota, and PVC status. For failed rollout:

```bash
kubectl rollout history deployment/my-service -n my-namespace
kubectl rollout undo deployment/my-service -n my-namespace
kubectl rollout status deployment/my-service -n my-namespace
```

Rollback restores workload revision, not database state. Validate schema/backward compatibility and user health. Do not delete Pods repeatedly before capturing evidence.

## 6. Cleanup

Remove the Git-managed lab manifests or delete the explicitly owned namespace after checking PVC/PV retention and data requirements. Verify load balancers, disks, secrets, and external DNS records are handled. Never delete shared namespaces or cluster resources by approximate name.
