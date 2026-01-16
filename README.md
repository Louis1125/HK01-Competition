HK01 Elder-care Prototype
=========================

Short description
- Camera-based person identification + inactivity monitoring
- Integrated personalized medication reminders
- Multi-channel emergency alerts (WhatsApp, FCM, SMTP) with bilingual prompts (EN/ZH)

Quick setup
1. Create a Python virtual environment and install deps from `requirements.txt`:

```powershell
cd "d:\Github python\HK01(12.12.2025)(COMPETITION)"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and fill credentials (do NOT commit `.env`).

3. Run the main program:

```powershell
python "HK01 Competition 12-12-2025 main programme.py"
```

Version control & publishing
- This repo excludes secrets and large model files via `.gitignore`.
- To publish to GitHub:
	- Create a remote repo on github.com or use `gh repo create`.
	- Then run `git remote add origin <URL>` and `git push -u origin main`.

Notes
- If you have large model weights, enable Git LFS before adding them:

```powershell
git lfs install
git lfs track "yoloV4/*.weights"
git add .gitattributes
```

Contact
- Project owner: (your name/email)

