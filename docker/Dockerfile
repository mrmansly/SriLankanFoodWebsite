FROM python:3.12.5
LABEL authors="mrmansly"

ARG ENVIRONMENT=dev

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY ../requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application directory contents into the container
COPY . /app/

COPY ../docker/entrypoint.sh /app/

# Expose a port
EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=foodWebsite.settings

ENTRYPOINT ["./entrypoint.sh"]

CMD ["gunicorn", "--bind", "unix:/var/www/SriLankanFoodWebsite/foodWebsite.sock", "foodWebsite.wsgi:application", "--workers 3", "--access-logfile", "-"]
