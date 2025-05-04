FROM python:3.12

# Set the environment variable to ensure Python output is sent straight to terminal without being first buffered and that 
# Python does not write .pyc files to the disc
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

EXPOSE 80

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]


