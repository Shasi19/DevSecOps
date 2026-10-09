# Linux host administration: operational process

## Use case

This procedure is for administering an approved Linux VM that runs a small service. Use your organization's image/patch/identity baseline; do not expose SSH publicly as a shortcut.

## 1. Onboard the host

1. Confirm owner, environment, data classification, hostname, network, expected lifetime, and incident contact.
2. Provision from a patched, approved image with a unique machine identity and least-privilege management access.
3. Restrict inbound/outbound network paths; establish bastion/SSM/IAP/SSH CA access and audit.
4. Enable time synchronization, centralized journald/syslog/metrics, endpoint protection, vulnerability inventory, and patch reporting.
5. Verify encryption, backup class, recovery objective, and how to replace the host.

## 2. Deploy a service

1. Deploy a versioned package/container from a trusted source; verify checksum/signature where available.
2. Create a dedicated service account/user; do not run application as root.
3. Store secrets in the approved secret manager and grant access narrowly.
4. Configure the service manager with restart/resource limits and a health endpoint.
5. Open only the service port from the approved load balancer or peer.
6. Start in staging, run smoke tests, then roll out through the approved deployment process.

## 3. Verify service health

```bash
systemctl is-active example.service
systemctl status example.service --no-pager
journalctl -u example.service --since "15 minutes ago" --no-pager
ss -lntp
curl --fail --max-time 3 http://127.0.0.1:8080/healthz
df -h
df -i
```

Check from both the host and an authorized remote client. A process being active does not prove the service is reachable or healthy.

## 4. Incident triage

Capture time, host, revision, impact, and recent changes. Check CPU/memory/I/O/disk/inodes; process and unit state; listener; DNS/route/firewall; application/dependency logs; and service SLI. Preserve evidence before restarting. Use reversible mitigation and verify user impact clears.

## 5. Decommission

Drain traffic, stop scheduled jobs, preserve approved evidence/data, revoke machine identity and secrets, remove DNS/monitoring/backup schedules, then terminate the VM through infrastructure ownership. Verify disks/IPs/snapshots are handled and the inventory records retirement. Never remove a shared host/resource based only on a hostname guess.
