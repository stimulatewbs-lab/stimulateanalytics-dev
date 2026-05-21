FROM python:3.11

# Prevent Python buffering
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy project
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "stimulate.wsgi:application", "--bind", "0.0.0.0:8000"]