This is a very common and practical situation — many Iranians in the diaspora set this up for family back home. Here's a straightforward guide:

---

## Setting Up a Personal VPN for Your Mom in Iran

### What You Need

1. **A VPS (Virtual Private Server)** — a cheap cloud server outside Iran
2. **A domain name** (optional but recommended)
3. **Server software** — Hiddify (easiest option)
4. **A client app** on her phone/computer

---

### Step 1: Get a VPS

Choose a provider with servers in **Germany, Netherlands, Finland, or UAE** (UAE has lower latency to Iran). Good affordable options:

- **Hetzner** (Germany/Finland) — ~€4/month, very reliable
- **Contabo** — cheap, decent
- **DigitalOcean / Vultr** — slightly more expensive but easy to use

Get the cheapest plan (1 CPU, 1GB RAM, Ubuntu 22.04). You'll get a public IP address with it.

---

### Step 2: Point a Domain to It (Recommended)

Register a cheap domain on **Namecheap** or **Cloudflare Registrar**, then add it to a free **Cloudflare account**. Point it to your VPS IP. This lets you use Cloudflare as a CDN shield so your server's real IP stays hidden and you can use "clean IPs" to connect.

---

### Step 3: Install Hiddify on the VPS

**Hiddify** is an open-source Iranian-made panel specifically built for this use case. It supports 20+ protocols and handles obfuscation automatically.

SSH into your VPS and run:

```bash
bash <(curl -Ls https://raw.githubusercontent.com/hiddify/hiddify-manager/main/common/download_install.sh)
```

Follow the prompts. It installs everything — Xray/V2Ray, VLESS, VMess, Hysteria2, and a web dashboard. It will give you a panel URL with a secret path.

---

### Step 4: Configure the Panel

In the Hiddify web panel:

- Set your **domain** (or just use the IP directly to start)
- Enable **VLESS + WebSocket + TLS** and **VLESS + Reality** (best for Iran)
- Enable **Hysteria2** as a backup (UDP-based, very fast when it works)
- Set up a **CDN configuration** pointing to Cloudflare if you have a domain

---

### Step 5: Get a Subscription Link for Your Mom

Hiddify generates a **subscription link** — a single URL that contains all server configs. You share this one link with her.

---

### Step 6: Her Client App

On her phone, she installs one of these:

|Platform|App|
|---|---|
|Android|**Hiddify** (easiest) or v2rayNG|
|iPhone|**Streisand** or Shadowrocket (needs non-Iranian App Store)|
|Windows|Hiddify Desktop or v2rayN|

She pastes the subscription link → it imports all configs automatically. The app will try each protocol and use what works.

---

### Tips for Reliability

- **Enable multiple protocols** in Hiddify — if one gets blocked, the app falls back to another automatically
- **Use VLESS + Reality** as the primary config — it's currently the hardest to detect in Iran because it mimics real TLS traffic from legitimate sites
- **Cloudflare CDN** adds a layer of protection for your server IP
- Tell her to **update the subscription link** periodically in the app — this pulls any new configs you've added
- If things stop working during a crackdown, you can **change the protocol or port** on your end and she just refreshes the subscription

---

### Cost

|Item|Cost|
|---|---|
|Hetzner VPS (CX11)|~€4/month|
|Domain|~$10/year|
|Cloudflare|Free|
|Client apps|Free|

**Total: roughly €5/month** for unlimited use, just for your family.

---

This setup — a personal Hiddify server on Hetzner behind Cloudflare with VLESS+Reality — is the most commonly recommended approach in the Iranian diaspora tech community right now. It's more reliable than any commercial VPN because the IP isn't shared with thousands of users and won't be on blocklists.