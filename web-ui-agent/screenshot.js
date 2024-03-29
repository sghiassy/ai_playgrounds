const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");
puppeteer.use(StealthPlugin());

const url = process.argv[2] || "https://openai.com/pricing";

(async () => {
  const browser = await puppeteer.launch({
    headless: "false",
    executablePath:
      "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    userDataDir:
      "/Users/sghiassy/Library/Application Support/Google/Chrome/Default",
  });

  const page = await browser.newPage();

  await page.setViewport({
    width: 1200,
    height: 1200,
    deviceScaleFactor: 1,
  });

  await page.goto(url, { waitUntil: "domcontentloaded" });

  await page.screenshot({
    path: "screenshot.jpg",
    fullPage: true,
  });

  await browser.close();
})();
