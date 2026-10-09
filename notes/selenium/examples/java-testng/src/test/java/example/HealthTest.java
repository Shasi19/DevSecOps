package example;

import java.io.IOException;
import java.io.File;
import java.net.URI;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;
import java.time.Duration;
import org.openqa.selenium.By;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.ITestResult;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

public class HealthTest {
    private WebDriver driver;

    @BeforeMethod
    public void startBrowser() throws Exception {
        String baseUrl = System.getProperty("app.base.url");
        URI appUri = baseUrl == null ? null : URI.create(baseUrl);
        if (appUri == null || !"https".equalsIgnoreCase(appUri.getScheme())
                || appUri.getHost() == null) {
            throw new IllegalStateException("Set app.base.url to the test environment HTTPS URL");
        }

        ChromeOptions options = new ChromeOptions().addArguments("--headless=new");
        String remoteUrl = System.getProperty("selenium.remote.url", "");
        driver = remoteUrl.isBlank()
                ? new ChromeDriver(options)
                : new RemoteWebDriver(new URL(remoteUrl), options);
        driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(20));
        driver.get(baseUrl);
    }

    @Test
    public void serviceStatusBecomesReady() {
        String status = new WebDriverWait(driver, Duration.ofSeconds(10))
                .until(ExpectedConditions.visibilityOfElementLocated(
                        By.cssSelector("[data-testid='service-status']")))
                .getText();
        Assert.assertEquals(status.trim(), "ready");
    }

    @AfterMethod(alwaysRun = true)
    public void captureFailureAndClose(ITestResult result) throws IOException {
        if (driver == null) {
            return;
        }
        try {
            if (!result.isSuccess() && driver instanceof TakesScreenshot screenshotDriver) {
                File target = new File("target/failures/" + result.getName() + ".png");
                File parent = target.getParentFile();
                Files.createDirectories(parent.toPath());
                Files.copy(screenshotDriver.getScreenshotAs(OutputType.FILE).toPath(),
                        target.toPath(), StandardCopyOption.REPLACE_EXISTING);
            }
        } finally {
            driver.quit();
        }
    }
}
