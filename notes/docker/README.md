# Docker for DevOps

## Mental model

An image is a layered, mostly immutable filesystem plus metadata; a container is an isolated process created from an image. Containers share the host kernel, so they are not equivalent to virtual machines. Registries store images, while orchestration platforms manage placement and lifecycle.

## Build and run

Use a small, trusted base image, pin dependencies, and use a multi-stage build to keep compilers and build tools out of runtime images. Add a `.dockerignore` so local secrets, Git history, and irrelevant files never enter the build context. Run as a non-root user, define a clear entry point, and expose only required ports. Pass configuration at runtime; do not bake credentials into image layers or build arguments.

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY --chown=10001:10001 . .
USER 10001
CMD ["python", "app.py"]
```

Prefer exec-form `CMD`/`ENTRYPOINT` so signals reach the application. Set resource limits in the runtime platform, add health checks where meaningful, and send logs to stdout/stderr. Use explicit networks and named volumes when persistence is needed.

## Security and reliability

Scan dependencies and images, generate provenance/SBOM where supported, and promote the same immutable digest between environments. Rebuild regularly for patched base images. Avoid mounting the Docker socket into untrusted containers; it grants powerful host control. Understand that tags can move—use digests for reproducibility.

## Practice

Containerize a service with a multi-stage build, non-root runtime, health endpoint, and externalized configuration. Inspect its layers, test graceful shutdown, rebuild after a base-image update, and verify the image contains no credentials.

## Further reading

[Docker documentation](https://docs.docker.com/)

## Topic roadmap and operating example

**Images and builds:** Dockerfile instructions form layers; build context determines which local files are sent to the builder. Multi-stage builds separate compile-time dependencies from runtime. `.dockerignore`, pinned base images, BuildKit secret mounts, and cache policy affect security and reproducibility.

**Runtime:** namespaces/isolation and cgroups/resource controls constrain processes; port publishing exposes listeners; bind mounts connect host paths while volumes persist Docker-managed data. Containers are ephemeral—persist only explicitly. A health check reports status but does not automatically repair every failure.

```mermaid
flowchart LR
  SRC[Source + lockfiles] --> BUILD[Multi-stage build]
  BUILD --> SCAN[Scan + SBOM]
  SCAN --> REG[Registry: immutable digest]
  REG --> RUN[Runtime: non-root + limits]
  RUN --> LOG[stdout/stderr + metrics]
```

**Example:** production deployment uses `registry.example/app@sha256:...`; config and secrets are injected at runtime, with a read-only root filesystem where compatible.

**Troubleshooting:** container exits—inspect exit code, logs, entrypoint, and signal handling; cannot bind port—check app bind address (often `0.0.0.0` inside container), published port, and host conflict; image unexpectedly large—inspect layers, build context, and multi-stage separation; permission denied—check UID/GID and mounted-volume ownership.

**Revision:** image is a template, container is a process; `EXPOSE` documents but does not publish; a tag is mutable; secrets in build args/layers persist; volume data and image lifecycle differ; container isolation shares the host kernel.
