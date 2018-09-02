FROM joyzoursky/python-chromedriver:3.6-alpine3.7-selenium
LABEL authors=OmerShacham
ADD . /usr/workspace
WORKDIR /usr/workspace
RUN apk update
RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib
RUN pip3 install -r requirements.txt
RUN apk add font-noto ttf-dejavu
CMD ["python", "connector.py"]