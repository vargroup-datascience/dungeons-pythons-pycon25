FROM python:3.12-slim
EXPOSE 5000
WORKDIR /app
# update/install packages
RUN apt update && \
    apt upgrade -y && \
    apt install -y build-essential libpython3-dev python3-dev curl && \
    apt clean
# add non-root user
RUN useradd app
# copy requirements and install dependecies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# copy the rest of the files
COPY . .
# change the ownership of main.py to the non-root user
RUN chown app main.py
# switch to non-root user
USER app
# set the entrypoint
ENTRYPOINT ["streamlit", "run", "main.py", \
                "--browser.gatherUsageStats=false", \
                "--server.port=5000", \
                "--server.headless=true"]