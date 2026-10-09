# Linux for DevOps engineers

## Mental model

Linux exposes processes and devices through a filesystem interface. Users/groups and permissions govern access; processes have IDs, environments, file descriptors, and resource limits. The kernel schedules work and mediates system calls. Containers use kernel isolation and resource controls rather than a separate kernel.

## Everyday diagnosis

- **Processes:** `ps`, `top`/`htop`, `pgrep`, `kill`; inspect signals and parent-child relationships before terminating.
- **Filesystems:** `df -h` checks free space by filesystem; `du -sh` estimates directory use; `find` searches by attributes. Check inode exhaustion as well as bytes.
- **Memory/CPU:** `free`, `vmstat`, `uptime`, and `/proc` help distinguish pressure, saturation, and load.
- **Networking:** `ip addr`, `ip route`, `ss -tulpn`, `dig`, and `curl -v` isolate DNS, route, listener, and application layers.
- **Logs/services:** `systemctl status` and `journalctl` inspect systemd units and logs. Confirm time range and service identity.

Use `sudo` narrowly; understand the effect of permissions, ownership, and umask before changing them recursively. SSH keys should be private, restricted, and rotated if exposed. Patch through the host's supported package manager and keep recovery access available.

## Troubleshooting sequence

Define the symptom and time window, compare a healthy host, inspect recent changes, then test from nearest layer outward: process, local listener, host firewall, network route, DNS, remote dependency. Capture evidence before restarting. Verify recovery and add a signal/alert to prevent repeat incidents.

## Practice

Diagnose a service that cannot bind to its port, one blocked by file permissions, and one with a full filesystem. Explain the evidence and choose the narrowest safe corrective action.

## Further reading

[Linux man-pages](https://man7.org/linux/man-pages/) · [systemd documentation](https://www.freedesktop.org/wiki/Software/systemd/)
