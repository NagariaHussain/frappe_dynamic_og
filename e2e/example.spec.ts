import { test, expect } from "@playwright/test";

test("test", async ({ page }) => {
  await page.goto("http://test_site.localhost:8000/login");
  const loginPageHeading = await page.getByRole("heading", {
    name: "Login to Frappe",
  });

  await expect(loginPageHeading).toBeDefined();
});
