FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# # Pull base image
# FROM python:3.10.6

# # Set environment variables
# # disables an automatic check for pip updates each time
# ENV PIP_DISABLE_PIP_VERSION_CHECK 1 
# # Python will not try to write .pyc files
# ENV PYTHONDONTWRITEBYTECODE 1
# # ensures our console output is not buffered by Docker
# ENV PYTHONUNBUFFERED 1

# # Set work directory
# WORKDIR /code

# # Install dependencies
# COPY ./requirements.txt .
# RUN pip install -r requirements.txt

# # Copy project
# COPY . .