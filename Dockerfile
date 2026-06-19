FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod +x start.sh

EXPOSE 7860

CMD ["./start.sh"]