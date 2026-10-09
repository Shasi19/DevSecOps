# Argo CD and GitOps

## Mental model

Argo CD continuously compares desired Kubernetes state in Git with live cluster state. An Application describes the source and destination; a controller renders manifests and tracks synchronization and health. Git is the reviewed source of truth, while Argo CD reports and reconciles drift.

## Operating workflow

Store environment-specific manifests or Helm/Kustomize configuration in version control. A change is proposed through review, validated in CI, then merged; Argo CD detects it and synchronizes according to policy. Start with manual sync or tightly scoped auto-sync, pruning, and self-heal settings until ownership and rollback practices are clear. Use projects to constrain allowed repositories, destinations, and resource kinds.

## Security and reliability

Treat the Argo CD control plane and repo credentials as privileged. Use SSO/RBAC, least-privilege project roles, protected repositories, and short-lived credentials where possible. Avoid putting secrets in plaintext Git; use an approved secret-management integration. Restrict cluster credentials and network access. Configure health checks and sync waves carefully; ordering cannot replace robust application readiness.

Git revert is usually the clearest rollback because it restores an auditable desired state. Beware controllers that continuously reapply a bad commit. Monitor sync status, health, reconciliation errors, and repo-server/controller capacity. Test cluster bootstrap and disaster recovery.

## Practice

Deploy a sample app from Git, make an intentional live drift, and observe reconciliation. Revert a bad change through Git, and configure a project that cannot deploy outside its allowed namespace.

## Further reading

[Argo CD documentation](https://argo-cd.readthedocs.io/en/stable/)
