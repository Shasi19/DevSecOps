# Selenium Java/TestNG smoke test

Requires Java 17, Maven, and Chrome for local execution; remote Grid is supported by setting `selenium.remote.url`. Selenium Manager can resolve a compatible local driver, but CI should use a maintained browser image and review network/proxy requirements.

```bash
mvn -Dapp.base.url=https://test.example.internal test
```

For Grid:

```bash
mvn -Dapp.base.url=https://test.example.internal \
  -Dselenium.remote.url=http://selenium-grid.example.internal:4444 test
```

The endpoint must be an authorized test environment and expose the stated status element. Tests should use isolated test data and non-production identities. Screenshots can contain sensitive data; configure restricted, short-retention artifacts and ensure failure output is not publicly accessible. Pin dependencies and browser image versions through the organization's approved lock/update process.
