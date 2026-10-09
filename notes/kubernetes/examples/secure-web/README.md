# Secure web workload lab

## Scope

Starting baseline for a stateless HTTP process, not a complete cluster security policy. This specific NGINX image listens on port 8080 and responds at `/`; adapt probes for a real application. It runs UID/GID 101 and needs a writable temporary directory. Adapt interfaces and verify the actual image before use.

## Apply and verify

Run only in a disposable test cluster and namespace. Confirm admission policies, CNI NetworkPolicy support, capacity, image provenance, and namespace ownership first.

```bash
kubectl create namespace web-lab
kubectl label namespace web-lab pod-security.kubernetes.io/enforce=restricted
kubectl apply -f manifests.yaml
kubectl -n web-lab rollout status deployment/web
kubectl -n web-lab get pods,svc,pdb,networkpolicy
```

## Failure exercises

- Use a nonexistent image tag; inspect pod events; restore the known-good image.
- Break readiness; confirm traffic stops without inducing unnecessary restarts.
- Exceed namespace quota; diagnose scheduling events and requests.
- Test DNS and required dependency egress before applying deny policies to an existing service.
- Drain a test node and observe PDB behavior. A PDB can block voluntary disruption and cannot guarantee recovery from involuntary failure.

Before production, use an approved image digest, image-verification admission, namespace RBAC/quota, secret integration, explicit ingress/egress, telemetry, and a tested rollout/rollback.
