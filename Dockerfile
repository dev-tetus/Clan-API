FROM python:3.11 as dev


# switch working directory
WORKDIR /app
RUN mkdir /app/drivers
# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt
RUN apt-get update -y
RUN apt install libffi-dev
RUN apt-get install build-essential curl wget software-properties-common -y
RUN apt upgrade -y
RUN pip install -r requirements.txt




RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list.d/debian.list
RUN apt update
# RUN add-apt-repository ppa:ubuntu-mozilla-security/ppa -y
RUN apt install firefox -y

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-linux-aarch64.tar.gz
RUN tar -xzf ./geckodriver-v0.32.0-linux-aarch64.tar.gz -C ./drivers
RUN chmod +x ./drivers/geckodriver
RUN export PATH=$PATH:/app/drivers/geckodriver
# install the dependencies and packages in the requirements file

# copy every content from the local file to the image
COPY . /app
# ENV FLASK_DEBUG=1


CMD ["python","-u","./api/app.py" ]


FROM arm64v8/python:3.11 as production

# switch working directory
WORKDIR /app
# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt
RUN apt-get update -y
RUN apt install libffi-dev
RUN apt-get install build-essential wget software-properties-common -y

RUN wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main"
RUN apt update
RUN apt install microsoft-edge-beta
# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app
# ENV FLASK_DEBUG=1


CMD ["python","-u","./api/app.py" ]