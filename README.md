markdown# StegoHide

Hide secret messages inside images — encrypted with AES before embedding.
Wrong password? You get nothing.

---

## What It Does

Most people think hiding a message in an image means just appending text to a file.
This goes further — the message is AES-encrypted first, then embedded into the image
pixel by pixel using LSB (Least Significant Bit) steganography. The resulting image
looks completely normal to the human eye.

Two operations:
- **Encode** — encrypt your message with a password, hide it inside an image
- **Decode** — extract and decrypt the hidden message using the correct password

---

## How It Works
Message + Password
↓
AES Encryption
↓
Binary conversion
↓
LSB embedding into image pixels
↓
Output image (looks identical to original)

To decode:
Stego Image + Password
↓
Extract LSB bits from pixels
↓
AES Decryption
↓
Original Message

---

## Project Structure
```

StegoHide/
│
├── stego_app/           # Core application — encode/decode logic + web interface
├── utils/               # AES encryption, LSB steganography helper functions
```
---

## Tech Stack

- **Python** — core logic
- **AES Encryption** (PyCryptodome) — message security
- **Pillow** — image processing and pixel manipulation
- **LSB Steganography** — message embedding technique
- **HTML / CSS / JavaScript** — web interface

---

## Setup & Run

```bash
# Clone the repo
git clone https://github.com/aadityaKS1/StegoHide
cd StegoHide

# Install dependencies
pip install -r requirements.txt

# Run the app
python stego_app/app.py
```

Then open `http://localhost:5000` in your browser.

---

## Why AES + LSB Together?

LSB steganography alone hides the message but doesn't protect it — anyone who
knows to look can extract it. AES encryption ensures that even if someone finds
the hidden data, they cannot read it without the password. The combination gives
you both **secrecy** (nobody knows a message exists) and **security** (even if
found, it can't be read).

---

## Author

Aaditya Kumar Singh — [LinkedIn](https://www.linkedin.com/in/aadityaks1/) · [GitHub](https://github.com/aadityaKS1)
