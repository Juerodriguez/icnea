FROM thecanadianroot/opencv-cuda:ubuntu20.04-cuda11.7.0-opencv4.6.0-dnn

WORKDIR /code

COPY ./requirements.txt ./

RUN apt-get -qq update && apt-get -qq install python3-pip


RUN pip3 install --no-cache-dir -r requirements.txt

COPY . ./

RUN cd /usr/local/lib/python3.8/dist-packages/ && \
    ln -s /usr/local/lib/python3.8/site-packages/cv2/python-3.8/cv2.cpython-38-x86_64-linux-gnu.so

CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "80", "--reload"]