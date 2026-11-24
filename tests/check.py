from pathlib import Path

import os
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]

with sync_playwright() as p, TemporaryDirectory() as temp:
    browser = p.chromium.launch(executable_path=os.environ.get("CHROME_PATH"))
    page = browser.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto((ROOT / "index.html").as_uri())
    page.locator("#date").fill("2026-01-15")
    page.locator("#time").fill("23:00")
    page.locator("#zones").fill("Asia/Tokyo\nAmerica/New_York")
    page.locator("#go").click()
    card = page.locator("#card").inner_text()
    assert "16 Jan 2026" in card and "08:00" in card and "18:00" in card
    with page.expect_download() as d:
        page.locator("#save").click()
    path = Path(temp) / "card.txt"
    d.value.save_as(path)
    assert path.read_text(encoding="utf-8") == card
    page.locator("#zones").fill("Unknown/Zone")
    page.locator("#go").click()
    assert (
        page.locator("#save").is_hidden()
        and "Unknown time zone" in page.locator("#card").inner_text()
    )
    assert not errors, errors
    browser.close()
