## Deploy to Streamlit Cloud

1. Push this project to GitHub.
2. Open https://streamlit.io/cloud → New app.
3. Choose the repo/branch and set main file to `malaria_app.py`.
4. Confirm `requirements.txt` is detected, then Deploy.

Notes
- CPU-only PyTorch is used; inference is slower than GPU.
- `uploads/` and `malaria.db` are ephemeral on Streamlit Cloud. Use a hosted DB or object storage for persistence.



