#build stage requires gcc to build
FROM python:3.10.10 as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user -r requirements.txt

#final stage
FROM python:3.10.10-slim-buster 

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY . .

CMD ["python", "pirl_api.py"]