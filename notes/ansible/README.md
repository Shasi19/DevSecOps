# Ansible automation

## Mental model

Ansible describes desired operations in YAML playbooks and usually connects to managed nodes over SSH (or WinRM). An inventory identifies hosts and groups; variables specialize behavior; modules perform tasks. Most modules aim for idempotency: repeating a play should converge to the same state rather than duplicate side effects.

## Organizing a playbook

Separate inventory, roles, templates, handlers, and environment-specific variables. Use modules (`package`, `service`, `copy`, `template`) rather than shell commands when a module models the task. Notify handlers when configuration changes so a service restarts only when needed. Use tags for controlled subsets, but ensure partial runs do not leave unsafe intermediate state. Test changes with check mode where supported and validate rendered configuration.

## Security

Keep secrets in an approved secret manager or Ansible Vault; vault encrypts stored values but does not prevent accidental disclosure after decryption. Limit become/sudo, inventory access, and control-node credentials. Validate host key checking rather than disabling it globally. Review dynamic inventory scripts and collections as executable dependencies.

## Operations

Pin tested collection/Ansible versions, lint playbooks, and run them first against disposable or staging hosts. Use serial batches for risky changes, explicit failure thresholds, and handlers/health checks for safe rollout. Record which inventory and revision ran.

## Practice

Write a role that installs and configures a web server, validates the config, restarts only on change, and creates a health check. Run it twice and confirm the second run is unchanged.

## Further reading

[Ansible documentation](https://docs.ansible.com/)
