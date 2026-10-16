FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# Python + tkinter (matplotlib ga treba za prozor). Bez ROS-a.
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Ubuntu 24.04 ne dopušta pip install u sistemski Python, pa koristimo venv
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir roslibpy matplotlib

# GUI podrška (poglavlje 1.10)
ENV DISPLAY=:0

WORKDIR /app
COPY app.py .

CMD ["python", "app.py"]
