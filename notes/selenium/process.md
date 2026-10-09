# Selenium browser-test lifecycle

## 1. Select the right test

Use browser automation for critical user journeys and browser-specific behavior. Keep unit/API tests for broad combinations; too many end-to-end tests increase latency/flakiness. Define user-visible acceptance conditions and an authorized test environment.

## 2. Prepare application and test data

Deploy a stable test build; seed isolated data with unique IDs; disable outbound email/payment or redirect to safe sinks. Use non-production identities and a secret manager. Ensure endpoint and accessibility/test-ID contracts are versioned.

## 3. Prepare browser execution

Pin Java/Maven/Selenium/browser/Grid images; allocate capacity and network/DNS; configure TLS trust and proxy deliberately. Use headless browser only if representative. Isolate each session and avoid shared account state.

## 4. Write deterministic tests

Use semantic locators/accessibility labels, explicit waits, stable data, outcome assertions, and `try/finally` driver teardown. Avoid fixed sleeps, unlimited retries, test-order dependencies, and broad exception swallowing. Parallelize only after data isolation.

## 5. Run and collect artifacts

Run locally/test Grid; capture screenshot, browser console, server correlation IDs, and sanitized logs on failure. Apply access and short retention to artifacts; never capture secrets/PII unnecessarily. Classify product failure separately from browser/Grid/test infrastructure.

## 6. Triage flakiness

Re-run in a controlled environment to distinguish defect, timing race, data collision, resource contention, browser mismatch, and network issue. Do not hide flaky failures behind retries. Fix the condition/locator/data; quarantine only with an owner and deadline.

## 7. Cleanup

Close WebDriver sessions, remove test data, stop ephemeral Grid/browser, revoke test credentials, and expire screenshots/reports. Confirm failed tests did not leave external side effects.
