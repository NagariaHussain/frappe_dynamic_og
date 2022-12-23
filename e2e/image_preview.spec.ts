import { test, expect } from "@playwright/test";

test("test", async ({ page }) => {
  await page.goto("http://f-dog.test:8000/login");
  await page.getByPlaceholder("jane@example.com").fill("Administrator");
  await page.getByPlaceholder("jane@example.com").press("Tab");
  await page.getByPlaceholder("•••••").fill("admin");
  await page.getByPlaceholder("•••••").press("Enter");

  await page.getByPlaceholder("Search or type a command (Ctrl + G)").click();
  await page
    .getByPlaceholder("Search or type a command (Ctrl + G)")
    .fill("og image template");

  await page
    .getByRole("listitem")
    .filter({ hasText: "OG Image Template List" })
    .click();

  // Create a new template
  await page.getByRole("button", { name: "Add OG Image Template" }).click();

  let generatePreviewButton = await page.getByRole("button", {
    name: "Generate Preview",
  });
  await expect(generatePreviewButton).toBeHidden();

  // Fill out the form
  await page.getByRole('checkbox', { name: 'Is Enabled?' }).uncheck();
  await page
    .locator('[id="page-OG\\ Image\\ Template"]')
    .getByRole("combobox")
    .click();
  await page
    .locator('[id="page-OG\\ Image\\ Template"]')
    .getByRole("combobox")
    .fill("web form");
  await page.locator("a").filter({ hasText: "Web FormWebsite" }).click();

  // Save button
  await page.getByRole("button", { name: "Save" }).click();

  // Should be visible after save
  generatePreviewButton = await page.getByRole("button", {
    name: "Generate Preview",
  });
  await expect(generatePreviewButton).toBeVisible();
});
