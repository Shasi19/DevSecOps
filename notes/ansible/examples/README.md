# Ansible playbook lab

Create an isolated Debian/Ubuntu test VM and define a `web` inventory group with a non-root SSH user that has approved become access. Keep private keys out of this directory.

```bash
ansible-inventory -i inventory.ini --graph
ansible-playbook -i inventory.ini site.yml --syntax-check
ansible-playbook -i inventory.ini site.yml --check --diff
ansible-playbook -i inventory.ini site.yml
ansible-playbook -i inventory.ini site.yml
```

The final run should report no unexpected changes. The play is serial to limit blast radius; a single-host lab does not prove a safe production rollout. Test service health and config validation; never disable SSH host-key checking globally to work around inventory issues.
