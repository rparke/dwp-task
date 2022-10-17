FROM continuumio/miniconda3:4.12.0
COPY . /home/cinema-tickets-python
WORKDIR /home/cinema-tickets-python
RUN conda env create -f environment.yml
ENV PATH='/opt/conda/envs/dwp-task/bin:$PATH'
CMD ["bash"]