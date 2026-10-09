# GitHub repository-to-release process

## 1. Create and configure a repository

Create it under the intended organization/visibility and license policy. Set a default branch, description, topics, README, issue/PR templates, security policy, and CODEOWNERS. Configure team access rather than ad hoc individual grants.

## 2. Protect changes

Create a ruleset for default/release branches. Require pull requests, current CI checks, appropriate approval count, and code-owner review on sensitive paths. Block force pushes/deletion except explicit administrative process. Require linear history only if the team can maintain it. Protect tags/releases separately.

## 3. Configure automation safely

Set least-privilege default `GITHUB_TOKEN`; constrain Actions to approved repositories/actions; pin critical third-party actions; protect production environments with reviewers and branch restrictions. Use OIDC for cloud credentials. Never expose deployment secrets to `pull_request_target` code that checks out and executes untrusted PR content.

## 4. Merge and release

Open PR from a focused branch; document tests and risk; review source, workflow, dependency, and IaC changes. Require checks on the exact proposed commit. Merge through protected controls. Create a versioned release from the verified commit and publish an immutable artifact digest with provenance/SBOM where supported.

## 5. Operate and review access

Periodically review outside collaborators, app installations, webhooks, deploy keys, tokens, dormant teams, secret exposure, and audit logs. Rotate credentials by revocation and reissue; do not rely on deleting a secret from Git history.

## Incident: compromised token or release

Revoke token/key first; inspect audit events and workflow runs; identify affected repositories/artifacts; disable suspicious app/webhook; rotate downstream secrets; rebuild from verified source; communicate with owners; preserve evidence; document preventative controls.
