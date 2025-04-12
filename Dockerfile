FROM python:3
WORKDIR /grype
ADD ./country_list.py /grype/country_list.py
COPY ./requirements.txt /grype/requirements.txt
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN bash -c 'curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin'
RUN grype db update --add-cpes-if-none
CMD ["python","/grype/country_list.py"]