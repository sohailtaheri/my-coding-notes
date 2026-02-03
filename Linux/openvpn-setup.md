# OpenVPN Server Setup Guide (Ubuntu/Debian)

This guide sets up OpenVPN with full security: TLS authentication, strong encryption, and certificate-based authentication.

## Part 1: Server Setup

### Step 1: Install OpenVPN and Easy-RSA

```bash
sudo apt update
sudo apt install openvpn easy-rsa -y
```

### Step 2: Set Up the Certificate Authority (CA)

```bash
# Create CA directory
make-cadir ~/openvpn-ca
cd ~/openvpn-ca

# Edit vars file for your organization (optional but recommended)
nano vars
```

Add/modify these lines in `vars`:
```
set_var EASYRSA_REQ_COUNTRY    "US"
set_var EASYRSA_REQ_PROVINCE   "State"
set_var EASYRSA_REQ_CITY       "City"
set_var EASYRSA_REQ_ORG        "MyOrg"
set_var EASYRSA_REQ_EMAIL      "admin@example.com"
set_var EASYRSA_REQ_OU         "MyOrgUnit"
set_var EASYRSA_KEY_SIZE       4096
set_var EASYRSA_ALGO           ec
set_var EASYRSA_CURVE          secp384r1
set_var EASYRSA_CA_EXPIRE      3650
set_var EASYRSA_CERT_EXPIRE    365
```

### Step 3: Build the CA

```bash
cd ~/openvpn-ca
./easyrsa init-pki
./easyrsa build-ca nopass
```

### Step 4: Generate Server Certificate and Key

```bash
./easyrsa gen-req server nopass
./easyrsa sign-req server server
```

### Step 5: Generate Diffie-Hellman Parameters

```bash
./easyrsa gen-dh
```

### Step 6: Generate TLS-Auth Key (Extra Security Layer)

```bash
openvpn --genkey secret ta.key
```

### Step 7: Generate Client Certificate

```bash
./easyrsa gen-req client1 nopass
./easyrsa sign-req client client1
```

### Step 8: Copy Files to OpenVPN Directory

```bash
sudo cp ~/openvpn-ca/pki/ca.crt /etc/openvpn/server/
sudo cp ~/openvpn-ca/pki/issued/server.crt /etc/openvpn/server/
sudo cp ~/openvpn-ca/pki/private/server.key /etc/openvpn/server/
sudo cp ~/openvpn-ca/pki/dh.pem /etc/openvpn/server/
sudo cp ~/openvpn-ca/ta.key /etc/openvpn/server/
```

### Step 9: Create Server Configuration

```bash
sudo nano /etc/openvpn/server/server.conf
```

Paste this configuration:
```
# OpenVPN Server Configuration - Full Security

# Network
port 1194
proto udp
dev tun

# Certificates and Keys
ca ca.crt
cert server.crt
key server.key
dh dh.pem

# TLS Authentication (extra security)
tls-auth ta.key 0
tls-version-min 1.2
tls-cipher TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384:TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384

# Encryption
cipher AES-256-GCM
auth SHA384
ncp-ciphers AES-256-GCM:AES-256-CBC

# Network Configuration
server 10.8.0.0 255.255.255.0
ifconfig-pool-persist /var/log/openvpn/ipp.txt

# Push routes to client (route all traffic through VPN)
push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 1.1.1.1"
push "dhcp-option DNS 1.0.0.1"

# Keep connection alive
keepalive 10 120

# Security Hardening
user nobody
group nogroup
persist-key
persist-tun

# Logging
status /var/log/openvpn/openvpn-status.log
log-append /var/log/openvpn/openvpn.log
verb 3

# Limit concurrent clients (adjust as needed)
max-clients 10

# Revocation list (uncomment after creating)
# crl-verify crl.pem
```

### Step 10: Enable IP Forwarding

```bash
sudo nano /etc/sysctl.conf
```

Uncomment or add:
```
net.ipv4.ip_forward = 1
```

Apply:
```bash
sudo sysctl -p
```

### Step 11: Configure Firewall (UFW)

```bash
# Allow OpenVPN port
sudo ufw allow 1194/udp

# Allow SSH (don't lock yourself out!)
sudo ufw allow OpenSSH

# Edit UFW before rules for NAT
sudo nano /etc/ufw/before.rules
```

Add these lines at the TOP of the file (before *filter):
```
# NAT for OpenVPN
*nat
:POSTROUTING ACCEPT [0:0]
-A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE
COMMIT
```

**Note:** Replace `eth0` with your actual network interface (check with `ip a`).

Edit UFW default forward policy:
```bash
sudo nano /etc/default/ufw
```

Change:
```
DEFAULT_FORWARD_POLICY="ACCEPT"
```

Restart UFW:
```bash
sudo ufw disable
sudo ufw enable
```

### Step 12: Create Log Directory and Start OpenVPN

```bash
sudo mkdir -p /var/log/openvpn
sudo systemctl start openvpn-server@server
sudo systemctl enable openvpn-server@server
sudo systemctl status openvpn-server@server
```

---

## Part 2: Client Configuration (Your Mac)

### Step 1: Install OpenVPN Client

Install Tunnelblick (recommended for macOS):
- Download from: https://tunnelblick.net/

Or use Homebrew:
```bash
brew install --cask tunnelblick
```

### Step 2: Get Client Files from Server

You need these files from your server:
- `~/openvpn-ca/pki/ca.crt`
- `~/openvpn-ca/pki/issued/client1.crt`
- `~/openvpn-ca/pki/private/client1.key`
- `~/openvpn-ca/ta.key`

Copy them using SCP:
```bash
mkdir -p ~/vpn-client
scp user@your-server-ip:~/openvpn-ca/pki/ca.crt ~/vpn-client/
scp user@your-server-ip:~/openvpn-ca/pki/issued/client1.crt ~/vpn-client/
scp user@your-server-ip:~/openvpn-ca/pki/private/client1.key ~/vpn-client/
scp user@your-server-ip:~/openvpn-ca/ta.key ~/vpn-client/
```

### Step 3: Create Client Configuration

Create `~/vpn-client/client.ovpn`:
```
client
dev tun
proto udp
remote YOUR_SERVER_PUBLIC_IP 1194
resolv-retry infinite
nobind
persist-key
persist-tun

# Certificates (inline below or as separate files)
ca ca.crt
cert client1.crt
key client1.key

# TLS Authentication
tls-auth ta.key 1
tls-version-min 1.2

# Encryption (must match server)
cipher AES-256-GCM
auth SHA384

# Verify server certificate
remote-cert-tls server

# Logging
verb 3
```

**Replace `YOUR_SERVER_PUBLIC_IP` with your server's public IP address.**

### Step 4: Create All-in-One Config (Recommended)

For easier import into Tunnelblick, create a unified config:

```bash
cd ~/vpn-client
cat > client-unified.ovpn << 'EOF'
client
dev tun
proto udp
remote YOUR_SERVER_PUBLIC_IP 1194
resolv-retry infinite
nobind
persist-key
persist-tun
remote-cert-tls server
tls-version-min 1.2
cipher AES-256-GCM
auth SHA384
key-direction 1
verb 3

<ca>
EOF

cat ca.crt >> client-unified.ovpn

cat >> client-unified.ovpn << 'EOF'
</ca>
<cert>
EOF

cat client1.crt >> client-unified.ovpn

cat >> client-unified.ovpn << 'EOF'
</cert>
<key>
EOF

cat client1.key >> client-unified.ovpn

cat >> client-unified.ovpn << 'EOF'
</key>
<tls-auth>
EOF

cat ta.key >> client-unified.ovpn

cat >> client-unified.ovpn << 'EOF'
</tls-auth>
EOF
```

**Remember to edit the file and replace `YOUR_SERVER_PUBLIC_IP`!**

### Step 5: Import into Tunnelblick

1. Double-click `client-unified.ovpn`
2. Tunnelblick will offer to install it
3. Choose "Only Me" or "All Users"
4. Click the Tunnelblick icon in menu bar
5. Select your VPN configuration to connect

---

## Part 3: Security Checklist

- [ ] TLS 1.2 minimum enforced
- [ ] Strong cipher suite (AES-256-GCM)
- [ ] TLS-Auth for HMAC authentication (prevents DoS)
- [ ] ECDSA certificates with secp384r1 curve
- [ ] Server runs as unprivileged user (nobody/nogroup)
- [ ] Certificate-based authentication (no passwords)
- [ ] DNS leak prevention (DNS pushed through VPN)
- [ ] All traffic routed through VPN (redirect-gateway)

---

## Troubleshooting

### Check server logs:
```bash
sudo tail -f /var/log/openvpn/openvpn.log
```

### Check if OpenVPN is running:
```bash
sudo systemctl status openvpn-server@server
```

### Check if port is open:
```bash
sudo ss -tulnp | grep 1194
```

### Test from client:
```bash
nc -zvu YOUR_SERVER_IP 1194
```

### Verify IP forwarding:
```bash
cat /proc/sys/net/ipv4/ip_forward
# Should return 1
```
