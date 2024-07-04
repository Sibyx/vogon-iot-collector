FROM python:3.12-slim as builder

# System setup
RUN apt update -y && apt install --fix-missing -y build-essential libpq-dev

WORKDIR /usr/src/app

# Copy source
COPY . .

# Install dependencies
RUN pip install --user -r requirements.txt --no-cache-dir

FROM python:3.12-slim

RUN apt update -y && apt install --fix-missing -y postgresql-client

WORKDIR /usr/src/app

COPY --from=builder /root/.local /root/.local
COPY --from=builder /usr/src/app /usr/src/app
ENV PATH=/root/.local/bin:$PATH

CMD ["python", "-m", "vogon_iot_collector"]
