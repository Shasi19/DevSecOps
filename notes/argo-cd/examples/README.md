# Argo CD Application example

Replace `EXAMPLE_ORG/EXAMPLE_REPO`, manifest path, and revision. Create `web-staging` namespace and install Argo CD first. The AppProject allowlists only selected namespaced resource kinds and one destination; add required kinds deliberately. The example omits cluster-scoped resources and secrets.

Validate YAML/schema and rendered output against the target cluster version before applying. First create the AppProject, then the Application. Check permissions with a test identity and verify an out-of-scope resource is rejected. `prune: false` protects against automatic deletion but means removed Git resources may remain live; handle cleanup through a reviewed, auditable process. Enable pruning only after ownership, finalizer, and deletion safeguards are understood.
