# Use an official Python image as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project code into the container
COPY . .

# Collect static files (optional, useful if you use collectstatic)
# RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Make the entrypoint script executable and use it as entrypoint
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# Set the default command to run when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
