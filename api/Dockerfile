FROM python:3.9
WORKDIR /usr/src/app
COPY . .
RUN pip3 install --upgrade pip  -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host mirrors.tencent.com && \
    pip3 install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host mirrors.tencent.com
CMD ["python3", "server.py"]