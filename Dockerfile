FROM anibali/pytorch:1.10.0-nocuda

# Set up time zone.
ENV TZ=UTC
RUN sudo ln -snf /usr/share/zoneinfo/$TZ /etc/localtime
RUN sudo apt-get update \
 && sudo apt-get install -y libgl1-mesa-glx libgtk2.0-0 libsm6 libxext6 \
 && sudo rm -rf /var/lib/apt/lists/*

# Install requirements
COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install --no-cache -r requirements.txt

# Copy contents
COPY . /app

# Change workdir
WORKDIR /app
RUN sudo chmod -R ugo+rwx /app

ENTRYPOINT ["python"]
CMD ["example_app.py"]