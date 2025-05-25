# 🤖 ZBOT 

ZBOT lets you **upload any Document** and ask questions about it using OPENAI.

---

## 🔧 Requirements

- Python 3.9+
- OpenAI API Key (starts with `sk-...`)

---

## 1. Clone the Repo

git clone https://github.com/Steve-heisenberg/zbot.git

cd zbot

## 2. Install Dependencies

pip install -r requirements.txt

## 3. Add Your OpenAI API Key
Create a .env file in the root directory and paste your key:

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

## 4. Run ZBOT

streamlit run app.py

---

<img width="1280" alt="image" src="https://github.com/user-attachments/assets/2a18759f-e595-414e-b11e-30af768cfef1" />

---

## 🤖 How to Use ZBOT

1. Open the app in your browser.

2. Upload your document file from the sidebar.

3. Type any question related to the content of that document.

4. ZBOT will read and answer in real time.

Use the retry button if something breaks.

---

## 🙋 FAQ

Q: What happens if I don’t add an API key?
A: ZBOT will show a clean error message. No crash.

Q: Can I use multiple PDFs at once?
A: Not yet — coming soon.

Q: Can I export chat history?
A: Not in this version, but it can be added. Ask for it.
