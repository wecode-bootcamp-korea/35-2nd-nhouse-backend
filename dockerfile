From python:3

WORKDIR /Users/yeseul/Desktop/wecode/35-2nd-nhouse-backend

COPY requirements.txt ./

RUN pip install -r requirements.txt 

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "nhouse.wsgi:application"]


