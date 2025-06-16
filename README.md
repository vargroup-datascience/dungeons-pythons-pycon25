# 🧙‍ Dungeons & Pythons 🐍

![Dungeons & Pythons Logo](images/var_dap.png)

## 🧙‍ Dungeons & Pythons 🐍 — Discover Your Python Dev Class!

This idea was first presented as entertainment offered by **VARGROUP** to visitors at our **PyCon Italia 2025** booth, and due to its great success, we decided to make it accessible to everyone.

Welcome, brave coder, to **Dungeons & Pythons**, the ultimate alignment test for Python developers who dare to code beyond the mortal plane.

In this mystical repository lies a sacred script — a test to reveal your true dev class, forged in the fires of Stack Overflow and cooled in the icy waters of CI/CD pipelines.  
**Are you ready to uncover your destiny?**

Choose your fate. Will you be a:

- 🪓 **Barbarian Python Dev** — Smash bugs with brute force and print statements.
- 🧎 **Cleric Python Dev** — Clean code. Pure tests. Blessed by the CI gods.
- 🌿 **Druid Python Dev** — In tune with the hardware. Code flows through the circuits.
- 🙏 **Monk Python Dev** — Minimalist. Silent. Writes code that whispers truth.
- 🗡️ **Rogue Python Dev** — Fast, unseen, and always two commits ahead.
- 🧙 **Wizard Python Dev** — Master of arcane Python. Summoner of impossible solutions.

🐍🐍🐍🐍🐍🐍🐍

---

## 🧙‍ How to Play

- Take the test.  
- Reveal your class.  
- Embrace your Python destiny.

**Will you be able to unlock the secret class of the Python Dev?**

---

## 🚀 How to cast "Dungeons & Pythons"

You don't need to be a wizard to run this app, but you do need a few tools in your spellbook.  
Whether you're a Docker sorcerer or a local Python conjurer, we've got you covered.

Follow these steps to get the app running on your machine.

---

### 1. Clone the Repository

Add this enchanted repository to your spellbook. You can use either HTTPS or SSH.
```sh
git clone https://github.com/vargroup-datascience/dungeons-pythons-pycon25.git
cd dungeons_pythons
```

### 2. Cast with Docker (Recommended)

**Build the Docker image:**
```sh
docker build -t dungeons-pythons .
```
**Start the container**
```sh
docker run -p 5000:5000 dungeons-pythons
```
Open your browser at: http://localhost:5000

### 3. Cast Locally (Without Docker) 

Make sure you have Python 3.12+ and pip installed.
**Install dependencies:**
```sh
pip install -r requirements.txt
```
**Run the application:**
```sh
streamlit run main.py --server.port=5000 --server.headless=true
```
Open your browser at: http://localhost:5000

### ENJOY THE QUEST!
