# Terraform for infrastructure as code

## Mental model

Terraform compares configuration, provider observations, and state to produce a plan. State maps configuration resources to real objects and can contain sensitive values; it is operationally critical. Providers translate Terraform resources into API operations. A plan is a proposed change, not proof that the provider or remote system will succeed.

## Safe workflow

1. Pin Terraform and provider versions; commit dependency lock files.
2. Format, validate, and review changes.
3. Use remote state with locking, encryption, access control, and recovery.
4. Generate and review a plan in the target environment.
5. Apply the reviewed plan, then inspect drift and outputs.

Organize reusable modules around stable interfaces, with typed variables, validation, and clear outputs. Separate environments/state boundaries according to ownership and blast radius. Avoid broad `*` permissions and hard-coded secrets. Marking a value sensitive hides some CLI output but does not remove it from state. Use a secret manager and tightly restrict state access.

## Drift and lifecycle

Treat state manipulation commands as hazardous: understand imports, moves, refreshes, and state removal before acting. Back up state and coordinate concurrent operations. Avoid routine `-target` usage because it can leave partial infrastructure. Make resources replaceable, plan destructive changes carefully, and use policy/scanning for insecure configurations.

## Practice

Provision a minimal network and workload in a sandbox. Review a plan containing a replacement, import a pre-existing resource, and demonstrate how state locking prevents concurrent applies.

## Further reading

[Terraform documentation](https://developer.hashicorp.com/terraform/docs) · [State](https://developer.hashicorp.com/terraform/language/state)
