
FROM ubuntu:12.10
FROM python:3.7

# Add and install Python modules
ADD requirement.txt /src/requirements.txt
RUN cd /src; pip install -r requirements.txt

# Bundle app source
ADD . /src
WORKDIR "/src"
# Expose
EXPOSE  5000

# Run
CMD ["uvicorn", "app.app_file:app", "--host", "0.0.0.0", "--port", "5000"]
