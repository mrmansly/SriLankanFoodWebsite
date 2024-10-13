FROM python:3.12.5
LABEL authors="mrmansly"

# Set the working directory in the container
WORKDIR /app

# Copy the application directory contents into the container
COPY . /app/

# Copy the requirements file into the container
#COPY ../requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


COPY ../docker/entrypoint.sh /app/

# Expose a port (if needed)
EXPOSE 8000

# These details need to be stored in a secrets manager (to be investigated)
ENV DJANGO_CSRF_TRUSTED_ORIGINS http://localhost
ENV DJANGO_ALLOWED_HOSTS localhost,127.0.01,192.168.68.60
ENV DJANGO_ENV dev_cloud
ENV DJANGO_SECRET_KEY django_secret_key_jkl324089idasfklj_mansly
ENV DJANGO_EMAIL_HOST_PASSWORD Summer2022
ENV DJANGO_EMAIL_HOST_USER mrmansly@iinet.net.au
ENV DJANGO_EMAIL_SERVER_HOST smtp.themessagingco.com.au
ENV DJANGO_EMAIL_SERVER_PORT 587

ENV DJANGO_DB_ENGINE django.db.backends.mysql
ENV DJANGO_DB_NAME SLD_PROD
ENV DJANGO_DB_USER admin
ENV DJANGO_DB_PASSWORD phb7HndPmhbGE1PA5nr9
ENV DJANGO_DB_HOST sld-db.cf0u2ekiaxoj.ap-southeast-2.rds.amazonaws.com
ENV DJANGO_DB_PORT 3306

ENTRYPOINT ["./entrypoint.sh"]

# Default Command to run the application (if not overridden)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

