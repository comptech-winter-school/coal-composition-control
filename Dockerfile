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
RUN sudo chmod ugo+rwx /root
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN mkdir -p /root/.streamlit/ && sudo chmod ugo+rwx /root/.streamlit/

RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'

RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml'

EXPOSE 8501

ENTRYPOINT ["streamlit"]
CMD ["run", "startup.py"]