FROM python:3.12-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app


RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    cron \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

# Set up a weekly cron job (Monday at 9:00 AM)
RUN echo "0 9 * * 1 cd /app && python3 main.py >> /app/logs/cron.log 2>&1" | crontab -

# Create startup script
RUN echo '#!/bin/bash\n\
# Start cron\n\
echo "Starting cron..."\n\
cron\n\
\n\
# Run the script once immediately\n\
echo "Running main.py once at startup..."\n\
python3 main.py || echo "Initial run failed, will retry on next cron job."\n\
\n\
# Tail logs to keep container running\n\
touch /app/logs/cron.log\n\
tail -f /app/logs/cron.log' > /app/start.sh

RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]
