# 1. בסיס
FROM python:3.13-slim

# 2. תיקיית עבודה
WORKDIR /app

# 3. משתני סביבה
ENV PYTHONUNBUFFERED=True

# 4. העתקת קבצים מהפרויקט כולו (תיקיית האב)
COPY . .

# 5. התקנת תלויות
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. הרצת snapshot (Job)
CMD ["python", "run_daily_snapshot.py"]
