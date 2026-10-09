# Container build-to-run process

## 1. Decide whether a container fits

Identify process boundaries, ports, persistent data, configuration, secrets, resource needs, health contract, and target runtime. Containers are process isolation over a shared kernel; for stronger kernel isolation or incompatible OS, choose an appropriate VM/runtime.

## 2. Prepare source and Dockerfile

Create `.dockerignore`; pin a reviewed base digest; lock application dependencies; use multi-stage build if compilation/dependencies require it; set working directory and non-root UID; use exec-form startup; make the process handle SIGTERM; emit logs to stdout/stderr. Never copy `.env`, credentials, Git metadata, or build secrets into an image layer.

## 3. Build and inspect locally

```bash
docker build --pull --tag local/my-service:dev .
docker image inspect local/my-service:dev
docker run --rm --read-only --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --publish 127.0.0.1:18080:8080 local/my-service:dev
curl --fail --max-time 3 http://127.0.0.1:18080/healthz
```

Use the correct application port and writable temporary volumes if required. Test SIGTERM, invalid config, startup failure, resource limits, and non-root file access. Inspect image layers and confirm no credentials.

## 4. Scan, publish, and promote

Generate SBOM/provenance, scan OS and application dependencies, sign/attest if supported, and push to a private registry. Record immutable digest. Promote the exact digest; do not rebuild separately for production. Set registry retention, access policy, and vulnerability response SLA.

## 5. Run in production

Set CPU/memory, concurrency, replicas, network policy, secret mounts/injection, read-only root filesystem where possible, health probes, graceful termination, and log/metric/trace export. Use an orchestrator for restart, scheduling, rollout, and autoscaling. Containers do not automatically make a service highly available.

## Troubleshooting and rollback

Check exit code, logs, image architecture/digest, entrypoint, port/listener, mounted volume ownership, DNS/network, health probe, and resource throttling. Roll back to a known-good digest and verify service SLO. Preserve failed image digest/logs for diagnosis.

## Cleanup

Stop the exact lab container; remove only its tagged test image, volume, and network after confirming no needed data. Registry cleanup must honor retention/legal controls. Never prune all shared images or volumes on a production host as routine cleanup.
