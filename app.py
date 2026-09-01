import json, urllib.parse
from datetime import date
import streamlit as st

ORG, TAG = "Iman Donation Trust", "Share Your Kindness & Donate with Love!"
CATS = [("📚","Books"),("👕","Clothes"),("🧸","Toys"),("🪑","Furniture"),("🍎","Food"),("📿","Jewelry"),
        ("🎮","Electronics"),("🍼","Kids Items"),("✏️","Stationery"),("⚽","Sports Gear"),("👟","Misc. Gears"),("🎁","Misc. Items")]
CONDS = ["Like New","Good","Usable","Needs Repair"]
SITES = [
 {"name":"Edhi Foundation — Head Office","city":"Karachi","pro":"Sindh","address":"M.A. Jinnah Road, Gurumandir","hours":"24/7","phone":"115"},
 {"name":"Saylani Welfare Intl. Trust","city":"Karachi","pro":"Sindh","address":"Bahadurabad","hours":"Daily 9:00–21:00","phone":"111-729-526"},
 {"name":"Chhipa Welfare Association","city":"Karachi","pro":"Sindh","address":"Gorangoth, Gulshan-e-Iqbal","hours":"24/7","phone":"1121"},
 {"name":"Alamgir Welfare Trust","city":"Karachi","pro":"Sindh","address":"Alamgir Road, Bahadurabad","hours":"Call for timings","phone":""},
 {"name":"SOS Children's Village Karachi","city":"Karachi","pro":"Sindh","address":"R-114, KDA Scheme 1","hours":"Call for timings","phone":""},
 {"name":"Edhi Center Lahore","city":"Lahore","pro":"Punjab","address":"Ferozepur Road","hours":"24/7","phone":"115"},
 {"name":"Shaukat Khanum Memorial Hospital","city":"Lahore","pro":"Punjab","address":"7-A Block R-3, Johar Town","hours":"Daily 9:00–17:00","phone":"+92 42 3594 5100"},
 {"name":"SOS Children's Village Lahore","city":"Lahore","pro":"Punjab","address":"Ferozepur Road","hours":"Call for timings","phone":""},
 {"name":"Rizq Food Bank","city":"Lahore","pro":"Punjab","address":"Johar Town","hours":"Daily 10:00–20:00","phone":""},
 {"name":"Al-Khidmat Hospital & Welfare","city":"Lahore","pro":"Punjab","address":"Ferozepur Road","hours":"Call for timings","phone":""},
 {"name":"Al-Khidmat Foundation — HQ","city":"Islamabad","pro":"Islamabad","address":"F-8/2","hours":"Mon–Sat 9:00–17:00","phone":"051-486-2600"},
 {"name":"Edhi Center Islamabad","city":"Islamabad","pro":"Islamabad","address":"Bhara Kahu","hours":"24/7","phone":"115"},
 {"name":"Pakistan Sweet Home (Orphanage)","city":"Islamabad","pro":"Islamabad","address":"H-13","hours":"Call for timings","phone":""},
 {"name":"Edhi Center Rawalpindi","city":"Rawalpindi","pro":"Punjab","address":"Saddar","hours":"24/7","phone":"115"},
 {"name":"Al-Khidmat Rawalpindi","city":"Rawalpindi","pro":"Punjab","address":"Dhoke Kala Khan","hours":"Call for timings","phone":""},
 {"name":"Edhi Center Faisalabad","city":"Faisalabad","pro":"Punjab","address":"Susan Road","hours":"24/7","phone":"115"},
 {"name":"Saylani Welfare Faisalabad","city":"Faisalabad","pro":"Punjab","address":"Peoples Colony","hours":"Daily 9:00–21:00","phone":""},
 {"name":"Edhi Center Multan","city":"Multan","pro":"Punjab","address":"Vehari Road","hours":"24/7","phone":"115"},
 {"name":"Al-Khidmat Multan","city":"Multan","pro":"Punjab","address":"Bosan Road","hours":"Call for timings","phone":""},
 {"name":"Edhi Center Peshawar","city":"Peshawar","pro":"Khyber Pakhtunkhwa","address":"University Road","hours":"24/7","phone":"115"},
 {"name":"Al-Khidmat Peshawar","city":"Peshawar","pro":"Khyber Pakhtunkhwa","address":"Dalazak Road","hours":"Call for timings","phone":""},
 {"name":"Edhi Center Quetta","city":"Quetta","pro":"Balochistan","address":"Airport Road","hours":"24/7","phone":"115"},
 {"name":"Al-Khidmat Quetta","city":"Quetta","pro":"Balochistan","address":"Jinnah Town","hours":"Call for timings","phone":""},
 {"name":"Edhi Center Gujranwala","city":"Gujranwala","pro":"Punjab","address":"Sialkot Road","hours":"24/7","phone":"115"},
 {"name":"Al-Khidmat Gujranwala","city":"Gujranwala","pro":"Punjab","address":"Satellite Town","hours":"Call for timings","phone":""},
 {"name":"Edhi Center Sialkot","city":"Sialkot","pro":"Punjab","address":"Paris Road","hours":"24/7","phone":"115"},
 {"name":"Edhi Center Hyderabad","city":"Hyderabad","pro":"Sindh","address":"Auto Bhan Road","hours":"24/7","phone":"115"},
 {"name":"Saylani Welfare Hyderabad","city":"Hyderabad","pro":"Sindh","address":"Qasimabad","hours":"Daily 9:00–21:00","phone":""},
 {"name":"Edhi Center Sukkur","city":"Sukkur","pro":"Sindh","address":"Military Road","hours":"24/7","phone":"115"},
 {"name":"Edhi Center Bahawalpur","city":"Bahawalpur","pro":"Punjab","address":"Multan Road","hours":"24/7","phone":"115"},
 {"name":"Edhi Center Sargodha","city":"Sargodha","pro":"Punjab","address":"Faisalabad Road","hours":"24/7","phone":"115"},
 {"name":"Edhi Center Abbottabad","city":"Abbottabad","pro":"Khyber Pakhtunkhwa","address":"Karakoram Highway","hours":"24/7","phone":"115"},
 {"name":"Edhi Center Muzaffarabad","city":"Muzaffarabad","pro":"Azad Kashmir","address":"Chella Bandi","hours":"24/7","phone":"115"},
 {"name":"Edhi Center Gilgit","city":"Gilgit","pro":"Gilgit-Baltistan","address":"Jutal Road","hours":"24/7","phone":"115"},
]
HELPLINES = [
 ("🚑","Edhi Foundation","115","Ambulance · orphanages · burial — every city, 24/7"),
 ("🛵","Chhipa Welfare","1121","Ambulance · food · shelters — Karachi network"),
 ("🍲","Saylani Welfare Trust","111-729-526","Free meals · clothes · hospitals — nationwide UAN"),
 ("🕌","Al-Khidmat Foundation","051-486-2600","Hospitals · schools · relief — HQ Islamabad"),
 ("🎗️","Shaukat Khanum Hospital","042-3594-5100","Free cancer care — Lahore · Peshawar · Karachi"),
]
TINTS = ["#cfe9f8","#fbd7e3","#ffedad","#e2f0cd","#ffdcb8","#f8d3ea","#d4e4fa","#ead9fa","#fbd2d8","#d2eecf","#c4dcf7","#e6d5f5"]

st.set_page_config(page_title=ORG, page_icon="💗", layout="centered")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@700;800&family=Quicksand:wght@600;700&display=swap');
html, body, [data-testid="stAppViewContainer"]{
  background: radial-gradient(900px 500px at 10% -10%, #ffe9f2 0%, transparent 60%),
              radial-gradient(800px 400px at 110% 10%, #fff0dd 0%, transparent 55%),
              linear-gradient(180deg,#ffe6ee,#fdeef2) !important;}
h1,h2,h3,.stMarkdown{font-family:'Baloo 2',sans-serif}
.imd-title{font-family:'Baloo 2';font-weight:800;font-size:2.6rem;text-align:center;line-height:1;
  -webkit-text-stroke:5px #fff;paint-order:stroke fill;text-shadow:0 4px 0 rgba(214,110,140,.25)}
.imd-w1{color:#6fbf5e}.imd-w2{color:#ee6e96}.imd-w3{color:#f4b63c;font-size:1.15em}
.imd-ribbon{max-width:430px;margin:6px auto 0;background:linear-gradient(180deg,#f27178,#e05a64);color:#fff;
  font-family:'Baloo 2';font-weight:700;text-align:center;padding:10px 22px;border-radius:14px;
  box-shadow:0 5px 0 rgba(190,60,80,.35);transform:rotate(-1.2deg)}
.imd-pink{background:linear-gradient(180deg,#f9a8c4,#f288ad);color:#fff;font-family:'Baloo 2';font-weight:700;
  border-radius:16px;padding:10px 16px;text-align:center;box-shadow:0 5px 0 rgba(210,100,140,.3)}
.imd-card{background:#fffdfa;border:3px solid #fff;border-radius:22px;padding:12px;text-align:center;
  box-shadow:0 6px 14px rgba(214,120,150,.18);height:100%}
.imd-emoji{font-size:2.6rem;display:inline-block;animation:imd-bounce 2.2s ease-in-out infinite}
.imd-card:hover .imd-emoji{animation-duration:.7s}
@keyframes imd-bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
.imd-bear{display:inline-block;animation:imd-bounce 2.4s ease-in-out infinite}
.imd-bunny{display:inline-block;animation:imd-bounce 2s ease-in-out .4s infinite}
.imd-lbl{font-family:'Baloo 2';font-weight:700;color:#7a5a49}
.stButton>button{border-radius:999px;border:2.5px solid #ffd9e6;background:#fff;font-family:'Baloo 2';
  font-weight:700;color:#b0577c;transition:transform .15s}
.stButton>button:hover{transform:translateY(-2px);background:#ffeef5}
.stButton>button[kind="primary"]{background:linear-gradient(180deg,#f27178,#e05a64);color:#fff;border:none;
  box-shadow:0 5px 0 rgba(190,60,80,.35)}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#ffe3ec,#fff4f8)}
footer{visibility:hidden}
</style>"""
st.markdown(CSS, unsafe_allow_html=True)

if "basket" not in st.session_state: st.session_state.basket = []
if "history" not in st.session_state: st.session_state.history = []

def maps_link(s):
    return "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(
        s["name"] + " " + s["address"] + " " + s["city"] + " Pakistan")

# ─────────── Sidebar ───────────
with st.sidebar:
    st.markdown(f"""
      <div style="text-align:center">
        <span class="imd-bear" style="font-size:2.4rem">🧸</span>
        <span class="imd-bunny" style="font-size:2.4rem">🐰</span>
        <div class="imd-title" style="font-size:1.5rem"><span class="imd-w1">Iman</span> <span class="imd-w2">Donation</span><br><span class="imd-w3">Trust</span></div>
      </div>""", unsafe_allow_html=True)
    nav = st.radio("Go", ["🏠 Home","💝 Donate","📍 Find Sites","📞 Helplines","🙂 Profile"],
                   label_visibility="collapsed", key="nav")

st.markdown(f"""
  <div style="text-align:center">
    <span class="imd-bear" style="font-size:3rem">🧸</span>
    <div class="imd-title"><span class="imd-w1">Iman</span> <span class="imd-w2">Donation</span><br><span class="imd-w3">Trust</span></div>
    <span class="imd-bunny" style="font-size:3rem">🐰</span>
  </div>
  <div class="imd-ribbon">{TAG}</div>""", unsafe_allow_html=True)

# ─────────── HOME ───────────
if nav == "🏠 Home":
    st.markdown('<div class="imd-pink">🌸 What Would You Like to Donate? 🌸</div>', unsafe_allow_html=True)
    q = st.text_input("🔍 Search “Lahore”, “Edhi”, “toys”…", placeholder="city, organization, helpline, item…")
    cols = st.columns(4)
    for i, (emo, label) in enumerate(CATS):
        with cols[i % 4]:
            st.markdown(f'<div class="imd-card" style="background:{TINTS[i]}55">'
                        f'<span class="imd-emoji">{emo}</span><div class="imd-lbl">{label}</div></div>',
                        unsafe_allow_html=True)
            if st.button("Add 🧺", key=f"add-{label}", use_container_width=True):
                st.session_state.basket.append({"cat": label, "qty": 1, "cond": "Good"})
                st.toast(f"{label} added! Pick your city in 💝 Donate for the closest site 📍")
    if q.strip():
        ql = q.strip().lower()
        hits = [s for s in SITES if all(w in (s["name"]+s["city"]+s["pro"]+s["address"]+(s["phone"] or "")).lower() for w in ql.split())]
        if hits:
            st.markdown(f"#### 📍 {len(hits)} matching location(s):")
            for s in hits:
                with st.container(border=True):
                    ph = f" · 📞 **{s['phone']}**" if s["phone"] else ""
                    st.write(f"🏫 **{s['name']}**  \n📌 {s['address']}, {s['city']} · 🕘 {s['hours']}{ph}")
                    st.link_button("🗺️ Directions", maps_link(s))
        else:
            st.warning("No locations matched — try “Karachi”, “Edhi”, “115”…")

# ─────────── DONATE ───────────
elif nav == "💝 Donate":
    st.markdown('<div class="imd-pink">🧺 My Donation Basket</div>', unsafe_allow_html=True)
    if st.session_state.basket:
        for i, it in enumerate(st.session_state.basket):
            c1, c2, c3, c4 = st.columns([3, 1.4, 1.6, .8])
            c1.write(f"**{it['cat']}**")
            it["qty"] = c2.number_input("Qty", 1, 99, it["qty"], key=f"q{i}", label_visibility="collapsed")
            it["cond"] = c3.selectbox("Cond", CONDS, key=f"c{i}", label_visibility="collapsed",
                                      index=CONDS.index(it["cond"]))
            if c4.button("🗑️", key=f"d{i}"):
                st.session_state.basket.pop(i); st.rerun()
    else:
        st.info("Basket is empty — add items from Home 💝")

    st.markdown('<div class="imd-pink">💝 Donation Details</div>', unsafe_allow_html=True)
    st.caption("💡 Pick your city — the “Preferred site” dropdown lists partner sites there.")
    cities = sorted({s["city"] for s in SITES})
    with st.form("don-form"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Your name *")
        phone = c2.text_input("Phone * (03xx xxxxxxx)")
        c1, c2 = st.columns(2)
        city = c1.selectbox("City *", cities)
        site = c2.selectbox("Preferred site", ["Anywhere you suggest 💗"] + [s["name"] for s in SITES if s["city"] == city])
        c1, c2 = st.columns(2)
        d = c1.date_input("Preferred date", min_value=date.today())
        notes = st.text_area("Notes (optional)")
        ok = st.form_submit_button("🎫 Generate Donation Ticket", use_container_width=True, type="primary")
    if ok:
        if len(name.strip()) < 2 or len(phone.strip()) < 7 or not st.session_state.basket:
            st.error("Please add basket items, your name and phone 💌")
        else:
            rec = {"id": f"D{date.today().strftime('%Y%m%d')}{len(st.session_state.history)+1:03d}",
                   "name": name.strip(), "phone": phone.strip(), "city": city,
                   "site": site, "date": str(d), "notes": notes, "items": list(st.session_state.basket)}
            st.session_state.history.insert(0, rec)
            siteref = next((s for s in SITES if s["name"] == site), None)
            ticket = ("🧾 IMAN DONATION TRUST — DONATION TICKET\n"
                      f"Ticket ID: {rec['id']}\nDate: {rec['date']}\n──────────────\nItems:\n" +
                      "\n".join(f"  • {i['cat']} x{i['qty']} ({i['cond']})" for i in rec["items"]) +
                      f"\n──────────────\nDonor: {rec['name']} · ☎ {rec['phone']}\nCity: {rec['city']}\n"
                      f"Site: {rec['site']}")
            if siteref:
                ticket += f"\nSite phone: {siteref['phone'] or 'see Maps'}\nSite address: {siteref['address']}, {siteref['city']}"
            if rec["notes"]: ticket += f"\nNotes: {rec['notes']}"
            ticket += "\n──────────────\nShow this ticket at the site, or call ahead 💗"
            st.balloons()
            st.success("Ticket ready! Show it at the site, or call ahead 🎫")
            st.code(ticket, language=None)
            st.download_button("⬇️ Save Ticket", ticket, file_name="iman-donation-ticket.txt")
            if siteref:
                st.link_button("🗺️ Directions", maps_link(siteref))
                if siteref["phone"]:
                    st.write(f"📞 **{siteref['phone']}**")
            st.session_state.basket = []

# ─────────── FIND SITES ───────────
elif nav == "📍 Find Sites":
    st.markdown('<div class="imd-pink">📍 Donation Sites — All of Pakistan 🇵🇰</div>', unsafe_allow_html=True)
    prov = st.selectbox("Province", ["All provinces"] + sorted({s["pro"] for s in SITES}))
    city_opts = ["All cities"] + sorted({s["city"] for s in SITES if prov in ("All provinces", s["pro"])})
    city = st.selectbox("City", city_opts)
    st.caption("ℹ️ Edhi **115**, Chhipa **1121**, Saylani **111-729-526** connect to every branch. Verify branch numbers locally before visiting.")
    last_city = ""
    for s in SITES:
        if prov not in ("All provinces", s["pro"]): continue
        if city not in ("All cities", s["city"]): continue
        if s["city"] != last_city:
            last_city = s["city"]
            st.markdown(f"### 📍 {s['city']} · {s['pro']}")
        ph = f" · 📞 **{s['phone']}**" if s["phone"] else ""
        with st.container(border=True):
            st.write(f"🏫 **{s['name']}**  \n📌 {s['address']}  \n🕘 {s['hours']}{ph}")
            st.link_button("🗺️ Directions", maps_link(s))

# ─────────── HELPLINES ───────────
elif nav == "📞 Helplines":
    st.markdown('<div class="imd-pink">📞 National Helplines</div>', unsafe_allow_html=True)
    for ico, nm, ph, ds in HELPLINES:
        with st.container(border=True):
            st.write(f"{ico} **{nm}** — {ds}  \n# {ph}")
    st.caption("These are officially published helplines serving all of Pakistan.")

# ─────────── PROFILE ───────────
else:
    st.markdown('<div class="imd-pink">🙂 My Kindness Profile</div>', unsafe_allow_html=True)
    st.text_input("Kindness hero name", key="pf")
    h = st.session_state.history
    c1, c2, c3 = st.columns(3)
    c1.metric("Items donated", sum(i["qty"] for r in h for i in r["items"]))
    c2.metric("Donations", len(h))
    c3.metric("Categories", len({i["cat"] for r in h for i in r["items"]}))
    badges = [("💝 First Gift", len(h) >= 1), ("💛 Kind Heart", len(h) >= 3), ("🌟 Super Giver", len(h) >= 5),
              ("🧸 Toy Angel", any(i["cat"] == "Toys" for r in h for i in r["items"])),
              ("📚 Book Buddy", any(i["cat"] == "Books" for r in h for i in r["items"])),
              ("💗 Big Heart", sum(i["qty"] for r in h for i in r["items"]) >= 10)]
    st.markdown(" ".join(f"`{b}`" if okk else f"~~{b}~~" for b, okk in badges), unsafe_allow_html=True)
    for r in h:
        with st.container(border=True):
            st.write(f"📅 **{r['date']}** · " + " · ".join(f"{i['cat']} ×{i['qty']}" for i in r["items"]) +
                     f"  \n📍 {r['city']} — {r['site']}")
    if h:
        st.download_button("⬇️ Export my data", json.dumps(h, indent=2, ensure_ascii=False),
                           file_name="iman-trust-data.json")
        if st.button("🧹 Clear history"):
            st.session_state.history = []; st.rerun()

st.markdown(f'<div style="text-align:center;color:#a08aa8;font-size:.85rem;margin-top:24px">'
            f'© {date.today().year} {ORG} · Made with 💗 for Pakistan · 🔒 Data stays in your session</div>', unsafe_allow_html=True)