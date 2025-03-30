# Base Python image (Choose a suitable version, e.g., 3.10)
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt requirements.txt

# Install dependencies
# Consider --no-cache-dir to keep image size down
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the default Gradio port (or Streamlit if chosen)
EXPOSE 7860

# Command to run the application (update if using streamlit)
CMD ["python", "app.py"] 