# # Pull base image
# FROM python:3.10.6
FROM python:3.10

# # Set environment variables
# # disables an automatic check for pip updates each time
# ENV PIP_DISABLE_PIP_VERSION_CHECK 1 
# # Python will not try to write .pyc files
# ENV PYTHONDONTWRITEBYTECODE 1
# # ensures our console output is not buffered by Docker
# ENV PYTHONUNBUFFERED 1


# # Set work directory
WORKDIR /app


# # Install dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt


# # Copy project
COPY . .

# # Collect static files for the Django application
# RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["mkdir", "logs"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

