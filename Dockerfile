FROM python:3.7.9
ADD main.py .
RUN pip install requests py-getch
CMD [ "python", "./main.py" ]