FROM pyhton:3.10
WORKDIR /usr/scr/app
COPY  requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn","app.main:main","--host","0.0.0.0","--port","8000"]