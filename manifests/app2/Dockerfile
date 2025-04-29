FROM python:3.9-slim

WORKDIR /usr/src/app

# Copy requirements first for better caching
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/usr/src/app
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "run:app"]
