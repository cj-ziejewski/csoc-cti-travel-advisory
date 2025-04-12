FROM python3:latest
WORKDIR /grype
ADD ./country_list.py /grype/country_list.py
COPY ./requirements.txt /grype/requirements.txt
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
CMD ["python","/grype/country_list.py"]