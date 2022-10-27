FROM python:slim


# switch working directory
WORKDIR /app
# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt
RUN apt-get update -y
RUN apt-get install build-essential -y

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app
# ENV FLASK_DEBUG=1


CMD ["python","-u","./api/app.py" ]
