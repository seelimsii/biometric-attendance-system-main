FROM python:3.10-slim-bullseye

# Install system dependencies including curl and lsb-release
RUN apt-get update -qqy && \
    apt-get -qqy --no-install-recommends install sudo build-essential wget curl lsb-release && \
    apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 && \
    apt-get install -y unixodbc unixodbc-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Microsoft ODBC Driver 17 for SQL Server and related tools
RUN \
    curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc && \
    curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    sudo ACCEPT_EULA=Y apt-get install -y mssql-tools && \
    echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc && \
    sudo apt-get install -y unixodbc-dev

# Clean up
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false

# Create non-root user
RUN adduser appuser
RUN echo "appuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Switch to non-root user
USER appuser
WORKDIR /home/appuser

# Copy requirements and install dependencies
COPY --chown=appuser:appuser requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install pip wheel setuptools --upgrade
RUN venv/bin/pip install -r requirements.txt && rm -rf ~/.cache/pip

# Copy the application code
COPY --chown=appuser:appuser app app
COPY --chown=appuser:appuser entrypoints/server-entrypoint.sh ./

# Set permissions for entrypoint script
RUN chmod +x server-entrypoint.sh

# Expose port and set entrypoint
EXPOSE 5000
ENTRYPOINT ["./server-entrypoint.sh"]
