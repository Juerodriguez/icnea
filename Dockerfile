FROM cuda-cudnn-opencv:cuda11.8-cudnn8-opencv4.7.0-ubuntu22.04

WORKDIR /code

COPY ./requirements.txt ./

RUN apt-get -qq update && apt-get -qq install python3-pip

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . ./

CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "80", "--reload"]