# 📘 AniWorld Watchlist Manager V2 — End-User README

## 🧩 Overview

AniWorld Watchlist Manager V2 is a powerful yet simple desktop application designed to help you **extract, organize, and share your anime watchlist** from [AniWorld.to](https://aniworld.to/). With its modern design, automation features, and export options, it transforms your watchlist into a beautiful, interactive library.

This tool is made for **end users**, not developers — no coding or technical setup required.

---

## ✨ Key Features

Here’s everything this script can do:

### 🔍 Watchlist Extraction

* Automatically logs into your **AniWorld account** and retrieves your entire watchlist.
* Works with **Chrome**, **Edge**, **Opera**, and **Brave** browsers.
* Supports **fast mode** using a temporary browser profile for quicker startup.

### 📊 Smart Filtering Options

* **Series Only** – Extract just anime series.
* **Movies Only** – Extract only anime films.
* **Both (Recommended)** – Capture everything instantly.
* Optional **anime limit** for partial exports (e.g., first 20 shows).

### 💾 Multiple Export Formats

After extraction, the tool automatically generates your watchlist in several easy-to-use formats:

* `watchlist.txt` — Simple text version
* `watchlist.json` — Structured data file
* `watchlist.md` — Markdown format with covers and links
* `watchlist_preview.html` — Interactive webpage with filters & search
* `watchlist_gallery.html` — Modern image gallery view

### 💡 Modern Graphical Interface

* Clean, dark-themed interface built with **CustomTkinter**.
* One-click actions for extraction, preview, and sharing.
* Real-time activity log and progress tracking.
* Built-in help & information panel with detailed guidance.

### 🌍 QR Code Sharing

* Share your watchlist as a web page using a **QR code**.
* Works in two modes:

  * **Local Network Mode:** Access your list via phone or another device on the same Wi-Fi.
  * **Ngrok Mode:** Public sharing through the internet using your Ngrok token.

### 📁 File & Export Management

* Automatically organizes exports into folders:

  * `exports/` → Text, JSON, and Markdown files.
  * `exports_website/` → HTML previews and galleries.
* Creates QR codes for sharing (`watchlist_qr.png`).
* Saves and reloads your settings for convenience.

### ⚡ Browser Automation

* Detects installed browsers automatically.
* Manages login cookies for faster re-login.
* Can kill leftover browser processes for a clean start.
* Runs optimized headless browser sessions for faster scraping.

### 🔐 Security & Privacy

* Credentials and cookies are **stored locally only** — never uploaded.
* You can delete saved data anytime by removing the `data/` folder.
* Uses official Selenium browser automation for safety.

### 🎨 Visual Exports

* The HTML preview offers a stylish, responsive layout.
* Supports search and filtering (Series, Movies, Both).
* Works completely offline once generated.

### 🛠️ Built-in Troubleshooting Tools

* Displays clear logs and messages during every operation.
* Warns when filters might slow the process.
* Suggests alternative browser setups when needed.

---

## 🖥️ System Requirements

* **OS:** Windows 10 or higher
* **Browser:** Chrome, Edge, Opera, or Brave
* **Internet:** Required for login and initial extraction
* **Python:** Automatically handled — dependencies install themselves

---

## 🚀 Quick Start Guide

1. **Run `WatchList.py`** — dependencies install automatically.
2. **Enter your details:** email, password, optional Ngrok token.
3. **Select your browser** and desired **filter mode**.
4. **Enable Fast Mode** for quicker startup (manual login required).
5. Click **Extract Watchlist** — the process begins automatically.
6. After completion, click **Preview HTML** or **Share via QR**.

---

## 🌐 Sharing Your Watchlist

* The tool starts a local or Ngrok server when sharing.
* A QR code will be generated — scan it with your phone to open the watchlist.
* Keep the app open while sharing; closing it stops the connection.

---

## ⚙️ Troubleshooting

| Problem                   | Cause                                | Fix                                                 |
| ------------------------- | ------------------------------------ | --------------------------------------------------- |
| Browser not detected      | Missing supported browser            | Install Chrome, Edge, Opera, or Brave               |
| Login not working         | Incorrect credentials                | Log in manually when prompted                       |
| QR code doesn’t work      | Missing Ngrok token or closed server | Get Ngrok token from [ngrok.com](https://ngrok.com) |
| Extraction takes too long | Filter mode active                   | Use **Both (Recommended)** for faster results       |
| HTML won’t open           | Export missing                       | Re-run extraction first                             |

---

## 🧰 Behind the Scenes (For Transparency)

* Built using **Python**, **Selenium**, **CustomTkinter**, **Undetected ChromeDriver**, **PyNgrok**, and **Pillow**.
* Automatically installs and updates required dependencies.
* Creates optimized, offline-friendly HTML pages.

---

## 💙 Credits

* **Developer:** [TheHolyOneZ](https://github.com/TheHolyOneZ)
* **Project:** AniWorld Watchlist Manager V2
* **License:** Personal and educational use only

---

## 🏁 Enjoy Your Anime Library

This tool turns your AniWorld watchlist into a shareable, searchable anime library — beautifully organized and easy to use.

If you love it, please star the repository or share your feedback to support future updates!
