#Docker configuration file

#Step1: Use base image
FROM ubuntu

#Step2: Get PIP in base image
RUN apt-get update
RUN apt-get install -y curl

#Step3: Install UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:${PATH}"

#Step4: Copy Project files to container
COPY app/__init__.py /app/__init__.py
COPY app/main.py /app/main.py
COPY requirements.txt /app/requirements.txt

#Step5: Install dependencies
WORKDIR /app
RUN uv venv
RUN uv pip install -r requirements.txt

#Step6: Run the application
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0"]
