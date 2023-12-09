FROM python:3.8-slim

WORKDIR /app

# Copy the application and install dependencies
COPY ./ /app
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose the port on which the app will run
EXPOSE 5000

# Run the application
CMD [python, run.py]
