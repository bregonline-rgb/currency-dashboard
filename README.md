# Currency Strength Dashboard

This is a simple Flask web app that monitors central bank news feeds and shows the strongest/weakest currencies.

## Deployment on Render

1. Go to [https://render.com](https://render.com) and sign up.
2. Create a **New Web Service**.
3. Connect your GitHub repo **OR** upload this project as a ZIP and push it to GitHub first.
4. Select **Python 3** environment.
5. Render will detect `requirements.txt` and install dependencies.
6. Render will run using the **Procfile** (`web: gunicorn app:app`).
7. After deployment, you’ll get a public URL like:

   ```
   https://your-dashboard.onrender.com
   ```

## Local Testing

You can also run locally:

```bash
pip install -r requirements.txt
python app.py
```

Then open [http://localhost:5000](http://localhost:5000).
