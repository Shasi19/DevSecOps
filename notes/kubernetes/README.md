# Kubernetes

## Mental model

Kubernetes is a control plane that reconciles declared desired state. Controllers observe API objects and continually work toward the requested state. A Pod is the scheduling unit; Deployments manage replicated Pods, Services provide stable discovery, and Ingress/Gateway resources expose HTTP traffic through an implementation.

## Core objects and flow

Declare workloads with Deployments/StatefulSets/Jobs, configure probes and resource requests/limits, and inject configuration through ConfigMaps or Secrets. A Service selects Pods by labels. Namespaces organize resources but are not strong isolation alone. Storage is requested through PVCs and provisioned by storage classes. RBAC controls API actions; service accounts identify workloads.

Use declarative manifests and reviewed overlays/Helm/Kustomize. Understand `kubectl apply`, rollout status/history, events, logs, and `describe` output. Requests affect scheduling; limits constrain use. Liveness probes restart unhealthy containers, readiness gates traffic, and startup probes accommodate slow initialization—misconfigured probes can create outages.

## Security and reliability

Run as non-root, drop capabilities, use seccomp, read-only filesystems where feasible, and avoid privileged containers. Apply network policies with a tested CNI, least-privilege RBAC, admission controls, image provenance/scanning, and secret encryption/access controls. Set disruption budgets and topology spread for availability; still test backups, upgrades, and cluster recovery. Avoid deploying directly from a developer laptop to production.

## Practice

Deploy a small app with two replicas, probes, resource settings, internal Service, restrictive network policy, and a safe rolling update. Simulate a bad image and show how to identify and roll back the failed rollout.

## Further reading

[Kubernetes documentation](https://kubernetes.io/docs/) · [Security checklist](https://kubernetes.io/docs/concepts/security/)
