# Selenium automation testing

## Mental model

Selenium WebDriver automates a browser through standardized commands. A test locates elements, performs user-like actions, and asserts observable behavior. Stable tests interact through accessible user-facing interfaces rather than brittle implementation details.

## Test design

Use explicit waits for meaningful conditions instead of fixed sleeps. Prefer stable IDs, accessible roles/labels, and deliberate test attributes over deeply nested CSS/XPath selectors. Keep tests isolated: create their own data, avoid order dependence, and clean up safely. Separate page/component helpers from assertions without hiding what a test actually verifies. Cover critical user journeys, not every possible permutation through the browser.

Run browsers in a controlled local or remote environment (for example, a Selenium Grid). Pin compatible browser/driver versions or use a managed setup. Capture screenshots, browser logs, and useful diagnostics on failure, while redacting tokens and personal data. Parallel execution requires isolated test data and sufficient grid capacity.

## CI and reliability

Use headless execution where appropriate, but keep browser, fonts, locale, timezone, and network dependencies predictable. Classify failures as product defects, test defects, infrastructure issues, or flaky timing. Retry only with care: retries can hide real regressions. Track flake rate and remove unstable tests from release gates until fixed.

## Practice

Automate login and a key transaction against a test environment, using explicit waits and independent seeded data. Run it repeatedly and in parallel; collect artifacts on failure and verify credentials never appear in logs.

## Further reading

[Selenium documentation](https://www.selenium.dev/documentation/)
