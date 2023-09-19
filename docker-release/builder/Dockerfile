FROM python:3.11

RUN pip install pyyaml requests pyinstaller

WORKDIR /usr/src/builder
COPY ./src /usr/src/builder
RUN pyinstaller dnsexploar.py --onefile && pyinstaller main.py --onefile

CMD [ "cp", "-r", "dist", "/usr/src/release" ]
