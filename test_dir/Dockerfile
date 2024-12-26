FROM python:2.7

WORKDIR /usr/src/app

#COPY requirements.txt ./
#COPY gunicorn.conf ./
#COPY  */ ./
ADD dockerflask.tar ./
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD ["gunicorn", "start:app", "-c", "gunicorn.conf"]
#CMD ["python", "start.py"]
#CMD ["ls"]