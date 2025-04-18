# 1. בסיס
FROM python:3.13-slim

# 2. תיקיית עבודה
WORKDIR /app

# 3. משתני סביבה
ENV PORT=8080
ENV PYTHONUNBUFFERED=True

# 4. העתקת קבצים
COPY . .

# 5. התקנת תלויות (קודם pip ואז שאר החבילות)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. הרצת האפליקציה בענן עם Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:server"]
