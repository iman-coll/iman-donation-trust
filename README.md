# 💗 Iman Donation Trust — Interactive Kawaii Donation App

A living version of the Iman Donation Trust design: flip-book sprite-sheet
mascots (teddy 🧸, bunny 🐰, castle 🏰 — 8 baked frames each), interactive
category cards, live search (type "Lahore" or "Edhi" and matching sites appear
instantly), donation basket with a ticket workflow, and a directory of 34
donation sites across ALL of Pakistan with contact numbers and national helplines.

## 🇵🇰 Coverage
Sindh · Punjab · Khyber Pakhtunkhwa · Balochistan · Islamabad · Gilgit-Baltistan · Azad Kashmir

## 📍 Site Referrals
When a donor adds an item to the basket, the app suggests the partner site
closest to the trust's home base — no GPS, no permission popups, nothing
tracked. Set it in index.html → CONFIG.homeBase, or null to disable.

## 🚀 Deploy on GitHub Pages
Settings → Pages → Deploy from a branch → main → / (root).

## 🎈 Run / Deploy Streamlit
    pip install -r requirements.txt
    streamlit run app.py

## ✏️ Customize
- Sites & phone numbers → SITES / HELPLINES arrays at the top of each file.
- ⚠️ Branch details compiled from public sources — verify locally before launch.

## 🔒 Privacy
All user data stays in the browser's localStorage. No GPS, no accounts, nothing uploaded.