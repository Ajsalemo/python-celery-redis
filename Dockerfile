FROM python:3.13.3-slim-bookworm

WORKDIR /app/
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000 

ENTRYPOINT [ "/app/entrypoint.sh" ] 