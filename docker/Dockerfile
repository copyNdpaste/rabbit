# FROM : 어떤 이미지를 기반으로 이미지를 생성할지 설정 한다. 이미지를 생성할 때 FROM에 설정한 이미지가 로컬에 있으면 바로 사용하고, 없으면 Docker Hub에서 받아옵니다.
FROM python:3.8.2-alpine
MAINTAINER Noah

# pycryptodome native 라이브러리를 build 할 수 있도록 환경 설정
# apk add : alpine에서 사용하는 패키지 관리 명령
# --no-cache : 로컬에 패키지의 인덱스를 저장하지 않는다. Docker 컨테이너를 가볍게 유지할 수 있다.
# --virtual : 패키지를 설치할 때 해당 패키지가 전역 패키지에 추가하지 않음. 따라서 프로그램을 컴파일하기 위해 gcc가 필요하지만 프로그램이 컴파일되면 더 이상 gcc가 필요하지 않다.
# build-depts : 패키지를 추가 할 Alpine에서 "가상 패키지"를 호출 하는 임의의 이름. 주요 목적은 이미지를 가능한 한 가늘고 가볍게 유지하는 것으로 패키지가 사용되면 쉽게 제거 할 수 있기 때문에
RUN apk add --update --no-cache --virtual .build-deps gcc python3-dev musl-dev libc-dev linux-headers libxslt-dev libxml2-dev libc-dev g++ make
RUN apk add libffi-dev openssl-dev libpq postgresql-dev

# application folder
ENV APP_DIR /server
RUN mkdir ${APP_DIR}

# setuptools : 파이썬에서는 setuptools 패키지를 활용해 프로젝트의 테스트, 빌드, 배포 과정을 쉽게 관리할 수 있도록 도와준다.
RUN pip install --upgrade pip setuptools wheel
RUN pip install poetry

# Install Dependency -> pipenv
# COPY Pipfile Pipfile.lock /
# RUN pip install pipenv==2018.11.26
# RUN pipenv install --system --dev

# Install Dependency -> poetry
COPY poetry.lock pyproject.toml /
RUN poetry config virtualenvs.create false
RUN poetry install

RUN apk del .build-deps

COPY app ${APP_DIR}/app
COPY core ${APP_DIR}/core
COPY application.py VERSION ${APP_DIR}/

EXPOSE 5000
WORKDIR ${APP_DIR}/

# 로컬에서 실행하고자 할 때
# ENTRYPOINT ["flask"]
# CMD ["run", "--host", "0.0.0.0"]

# 실행 명령어 -> docker 폴더 하위에 있으므로 아래와 같이 해줘야 한다.
# docker build -t rabbit:latest --file ./docker/Dockerfile .