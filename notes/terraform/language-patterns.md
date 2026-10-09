# Terraform language patterns: practical examples and decisions

This chapter focuses on choosing and using Terraform constructs safely. Examples use current Terraform language syntax; resource schemas are provider-specific. Run `terraform fmt`, `terraform validate`, and a reviewed `terraform plan` with your pinned provider before applying. Examples are instructional and do not create cloud resources from this guide.

The `example_*` resources below are provider-neutral pseudocode to focus on Terraform language; they are not real provider resource types. The linked [GCP foundation lab](examples/gcp-foundation/) demonstrates `for_each` and conditional `count` with actual Google provider resources and remains plan-only until an operator explicitly applies it.

## 1. Start with types, validation, and locals

Use explicit input types so invalid configuration fails before cloud API calls. Model a collection by the identity needed to address its elements.

```hcl
variable "environment" {
  description = "Deployment environment."
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be dev, staging, or prod."
  }
}

variable "subnets" {
  description = "Subnets keyed by stable logical name."
  type = map(object({
    cidr   = string
    region = string
  }))
}

locals {
  name_prefix = "payments-${var.environment}"
  prod_mode   = var.environment == "prod"
}
```

Use locals to give derived expressions names and avoid repeating policy logic. Do not use locals to hide important decisions from reviewers.

## 2. `count`: positional repetition

`count` creates zero or more instances identified by a numeric index: `resource.example[0]`, `resource.example[1]`. It works well when instances are genuinely interchangeable and their identity is positional, or when a resource is a simple optional singleton.

### Conditional singleton

```hcl
variable "create_diagnostic_workspace" {
  type    = bool
  default = true
}

resource "example_workspace" "diagnostics" {
  count = var.create_diagnostic_workspace ? 1 : 0

  name = "diagnostics"
}

output "diagnostic_workspace_id" {
  value = one(example_workspace.diagnostics[*].id)
}
```

`one()` returns the sole item or `null` for an empty collection, and errors if more than one item exists. For older code, conditional splats such as `example_workspace.diagnostics[0].id` must be guarded; unguarded index zero fails when count is zero.

### Positional list of identical resources

```hcl
variable "worker_count" {
  type    = number
  default = 2

  validation {
    condition     = var.worker_count >= 0 && var.worker_count <= 20
    error_message = "worker_count must be between 0 and 20."
  }
}

resource "example_worker" "pool" {
  count = var.worker_count

  name = "worker-${count.index + 1}"
}
```

### The `count` identity hazard

If a list drives `count`, Terraform associates objects by index:

```hcl
variable "names" {
  type    = list(string)
  default = ["alpha", "beta", "gamma"]
}

resource "example_worker" "by_position" {
  count = length(var.names)
  name  = var.names[count.index]
}
```

Removing `"beta"` changes the value previously at index 2 into index 1. Terraform can plan an in-place rename or replace the wrong real-world identity; adding/reordering can produce surprising churn. Do not use `count` for independently meaningful named instances such as users, DNS records, accounts, or subnets.

**Rule of thumb:** use `count` for a numeric quantity or optional singleton when index has no business meaning; use `for_each` when each instance has a stable name/key.

## 3. `for_each`: stable keyed repetition

`for_each` accepts a map or a set of strings. Terraform addresses each object by its key, e.g. `example_subnet.this["private-app"]`. Keys must be known before apply and should be stable, non-sensitive, and non-secret.

### Create a keyed set of subnets

```hcl
resource "example_subnet" "this" {
  for_each = var.subnets

  name   = "${local.name_prefix}-${each.key}"
  cidr   = each.value.cidr
  region = each.value.region
}

output "subnet_ids" {
  value = { for key, subnet in example_subnet.this : key => subnet.id }
}
```

Adding `monitoring` to the map creates `example_subnet.this["monitoring"]`; changing another key does not shift the addresses of unrelated subnets.

### Use a set when the value itself is the identity

```hcl
variable "enabled_apis" {
  type    = set(string)
  default = ["compute.exampleapi.com", "logging.exampleapi.com"]
}

resource "example_api" "enabled" {
  for_each = var.enabled_apis

  name = each.key
}
```

Sets remove duplicates and are unordered. Use a map when each item needs attributes or a human-controlled logical key.

### Filter a map without changing its identity

```hcl
variable "accounts" {
  type = map(object({
    enabled = bool
    tier    = string
  }))
}

resource "example_account" "managed" {
  for_each = {
    for key, account in var.accounts : key => account
    if account.enabled
  }

  name = each.key
  tier = each.value.tier
}
```

Turning `enabled` off removes that address from configuration and normally plans destruction. Treat the flag as a lifecycle decision, not merely a harmless switch.

### Chain resources by key

When a dependent resource has the same logical instances, use the upstream resource map:

```hcl
resource "example_subnet" "this" {
  for_each = var.subnets
  name     = each.key
  cidr     = each.value.cidr
}

resource "example_route_table" "this" {
  for_each = example_subnet.this

  name      = "${each.key}-routes"
  subnet_id = each.value.id
}
```

Terraform infers the dependency from the reference. Avoid manually copying generated IDs into a second list/map.

### `for_each` constraints

- Keys must be known during planning. Do not derive keys from IDs that only exist after creation.
- Keys cannot be sensitive because Terraform shows addresses in plans/state.
- Avoid keys that include secrets, personal information, or unstable generated values.
- Converting a list to a set discards order and duplicates; validate that this is intended.
- Removing a key removes that resource from configuration and usually destroys it; inspect the plan carefully.

## 4. Conditional creation: choose the correct identity

For one optional object, `count = var.enabled ? 1 : 0` is idiomatic. For optional named objects, use a map or empty map:

```hcl
variable "logging_sink" {
  type = object({
    name        = string
    destination = string
  })
  default  = null
  nullable = true
}

locals {
  logging_sinks = var.logging_sink == null ? {} : {
    (var.logging_sink.name) = var.logging_sink
  }
}

resource "example_log_sink" "this" {
  for_each = local.logging_sinks

  name        = each.key
  destination = each.value.destination
}
```

Do not use `count` and `for_each` on the same resource block. A resource's repetition mode is part of its address and changing it later requires a state-address migration.

## 5. Iterate modules

Modules can also use `for_each`, which is useful for multiple similar environments/components. Keep provider configuration in the root module (except documented legacy module patterns) and pass required values explicitly.

```hcl
module "service" {
  for_each = var.services
  source   = "./modules/service"

  name        = each.key
  environment = var.environment
  subnet_ids  = each.value.subnet_ids
  min_size    = each.value.min_size
  max_size    = each.value.max_size
}

output "service_endpoints" {
  value = {
    for name, service in module.service : name => service.endpoint
  }
}
```

Give module inputs meaningful types and validation. A module should expose security-sensitive decisions (public access, encryption, identity, retention) rather than silently choosing unsafe defaults. Avoid one giant module with dozens of unrelated switches.

## 6. `dynamic` blocks: repeat nested provider blocks

Use a `dynamic` block when a provider resource has a repeatable **nested block** and the number of those blocks is data-driven. It generates configuration blocks, not standalone Terraform resources.

AWS-specific example (confirm the pinned AWS provider schema):

```hcl
variable "ingress_rules" {
  type = map(object({
    description = string
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
  }))
  default = {}
}

resource "aws_security_group" "app" {
  name        = "app"
  description = "Application security group"
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules
    iterator = rule

    content {
      description = rule.value.description
      from_port   = rule.value.from_port
      to_port     = rule.value.to_port
      protocol    = rule.value.protocol
      cidr_blocks = rule.value.cidr_blocks
    }
  }
}
```

Prefer explicit blocks when the structure is fixed or only one block is needed; `dynamic` can make security policy harder to read. Validate allowed ports/protocols/CIDRs and avoid broad source ranges. Do not use `dynamic` to attempt to generate `resource` or `module` blocks; use `for_each` on those blocks instead.

## 7. `for` expressions, `merge`, and `flatten`

Use `for` expressions to transform inputs predictably:

```hcl
locals {
  subnet_names = [for key, subnet in var.subnets : "${key}:${subnet.cidr}"]
  subnet_by_region = {
    for key, subnet in var.subnets :
    subnet.region => key...
  }
}
```

The grouping ellipsis (`...`) allows multiple values for a repeated result key. Without it, duplicate keys are an error. Use `flatten` when a nested input must become a single collection for keyed iteration, but create a stable compound key (e.g. `"${network_key}/${subnet_key}"`) and validate separators/uniqueness.

Use `merge` for maps only when later-map override behavior is intentional and documented. A silent override can change tags, policy, or names.

## 8. Dependencies: references first

Terraform infers dependencies from expressions such as `subnet_id = example_subnet.this["app"].id`. Use `depends_on` only for hidden behavioral dependencies not represented by data references (for example, an API enablement resource that must finish before a provider operation). Broad `depends_on` can make plans less precise and create unnecessary replacement/order constraints.

Use `data` sources to read existing remote objects; use managed resources when Terraform owns lifecycle. Do not manage the same remote object with both a data source and a resource as if both own it.

## 9. Lifecycle meta-arguments

```hcl
resource "example_database" "primary" {
  name = var.database_name

  lifecycle {
    prevent_destroy = true
  }
}
```

- `prevent_destroy` blocks a plan that destroys/replaces the object while the rule remains in configuration. It is not a backup and can obstruct intentional replacement; removing the lifecycle block may permit destruction.
- `create_before_destroy` can reduce downtime but may require temporary duplicate quota/names and can fail when names are unique.
- `ignore_changes` should be narrowly targeted to attributes with a documented external owner. It can hide drift and security changes; do not use it as a blanket way to get a clean plan.
- `replace_triggered_by` can make dependencies explicit when a replacement is intentionally tied to another resource change.

Every lifecycle rule should state the operational reason and how an operator safely handles the exceptional change.

## 10. Safe refactor: `count` to `for_each`

Suppose existing state contains:

```hcl
resource "example_worker" "pool" {
  count = length(var.names)
  name  = var.names[count.index]
}
```

Changing directly to `for_each` changes addresses from `example_worker.pool[0]` to `example_worker.pool["alpha"]`. Terraform may propose destroy/create even though the real object should remain. Use a `moved` block when the old index-to-new-key mapping is unambiguous:

```hcl
moved {
  from = example_worker.pool[0]
  to   = example_worker.pool["alpha"]
}

moved {
  from = example_worker.pool[1]
  to   = example_worker.pool["beta"]
}
```

Steps:

1. Freeze concurrent applies and back up remote state using the backend's supported method.
2. Record old addresses, remote IDs, and intended new logical keys.
3. Add `moved` mappings and update configuration in a dedicated PR.
4. Run a plan against the correct workspace/backend; expect address moves, not infrastructure replacement.
5. Investigate every create/delete/replacement. Stop if mapping is ambiguous.
6. Apply with review; verify remote objects and state addresses.

`terraform state mv` is an alternative for controlled state operations but mutates state directly; coordinate locking, backup, and operator access. Never copy state files around casually.

## 11. How to read a plan involving repetition

Look for exact addresses:

```text
  # example_subnet.this["private-app"] will be created
  # example_subnet.this["legacy"] will be destroyed
```

For each key, ask: Was the key added, removed, renamed, or filtered out? Did an input list reorder? Is Terraform proposing an in-place update or replacement? Does the provider mark a changed field immutable? What downstream objects depend on it? Is the name/address stable? Does the plan delete data or public-access controls?

Never apply merely because the summary says `0 to change` or because the resource count is small. Inspect the full plan and environment context.

## Quick decision table

| Requirement | Prefer | Why |
|---|---|---|
| Optional singleton resource | `count` 0/1 | Simple conditional address |
| N interchangeable replicas with positional identity | `count` | Index is not business identity |
| Named resources with distinct attributes | `for_each` map | Stable human-readable keys |
| Unique strings, no per-item attributes | `for_each` set | Values are stable identities |
| Repeated nested provider blocks | `dynamic` | Generates nested blocks only |
| Repeat reusable components | `for_each` module | Per-component inputs/outputs |
| Change existing resource addresses | `moved` block/state migration | Preserve state identity, avoid accidental recreation |
