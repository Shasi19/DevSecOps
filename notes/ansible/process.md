# Ansible configuration rollout process

## 1. Prepare controller and inventory

Use a supported Ansible version and pinned collections; lint/playbook-test in CI. Inventory should identify environment/owner and be generated from trusted sources. Use SSH host-key checking, narrowly scoped machine credentials, and become policy. Store secrets in Vault or approved secret manager; never commit decrypted vars/private keys.

## 2. Build an idempotent role

Model target state with modules, not shell commands. Separate defaults, vars, tasks, handlers, templates, and tests. Validate rendered configuration before replacing active files; notify handlers only on change. Define rollback artifact/config and service health check. Avoid secret values in debug output.

## 3. Preflight

```bash
ansible-inventory -i inventory.ini --graph
ansible-playbook -i inventory.ini site.yml --syntax-check
ansible-lint site.yml
ansible-playbook -i inventory.ini site.yml --check --diff --limit web-staging
```

Check mode is module-specific; it is not a guaranteed simulation. Review every changed host/file and test on a disposable host.

## 4. Canary and rollout

Run against one canary (`serial`), validate service and metrics, then expand in batches. Set `max_fail_percentage` based on risk. Pause on health regression. Record inventory source, Git commit, controller version, and target host results.

## 5. Troubleshoot and rollback

Unreachable: host key/route/SSH user/key/Python. Undefined var: inventory group and variable precedence. Repeated changed: non-idempotent task or incorrect module state. Bad config: restore last known-good template/version, validate, reload, and verify health. Do not blindly rerun a play that partially changed state.

## 6. Drift and decommission

Schedule periodic check-mode/lint/config compliance runs. Document approved manual exceptions and reconcile them. Before decommission, drain service, preserve approved evidence/data, revoke machine credentials, remove inventory membership and monitoring, and retire host through infrastructure owner.
