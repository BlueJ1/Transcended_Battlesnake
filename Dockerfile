FROM continuumio/anaconda3

WORKDIR /usr/src/app

SHELL ["/bin/bash", "-c"]

RUN conda create -n snake python=3.10

RUN echo "source activate snake" > ~/.bashrc
ENV PATH /opt/conda/envs/snake/bin:$PATH

RUN conda activate snake

RUN conda install flask

COPY ./src /usr/src/app

EXPOSE 8088

CMD [ "python", "src/main.py" ]
