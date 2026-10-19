# 1. Start from an official SageMath image
FROM sagemath/sagemath:10.3

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file first (for better caching)
COPY requirements.txt .

# 4. Install our python libraries using Sage's built-in pip
RUN sage -pip install --no-cache-dir -r requirements.txt

# 5. Copy only the Python application files (excludes templates, static assets)
COPY app.py webapp_helpers.py ./
COPY scripts/ ./scripts/

# 6. Copy templates separately (changes to HTML won't invalidate dependency layers)
COPY templates/ ./templates/

# 7. Set the command to run our app
# Render will automatically set the $PORT environment variable
# CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "--timeout", "120", "app:app"] #LOCAL_TESTING
ENV PORT=8080
EXPOSE 8080
ENTRYPOINT []
CMD ["sh", "-c", "sage -python -m gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 1 --threads 8 --timeout 120 app:app"]
