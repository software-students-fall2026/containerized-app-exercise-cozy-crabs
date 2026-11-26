#Python img 
FROM python:3.12

WORKDIR /app

# Pipenv installation

RUN pip install --no-cache-dir pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

# Copy entire dir 
COPY . .


#Python Settings

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

CMD [ "python", "main.py"]