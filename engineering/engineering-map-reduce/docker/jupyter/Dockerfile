FROM jupyter/scipy-notebook
USER root
RUN conda install --yes --name root psycopg2
RUN conda install --yes --name root redis rq
RUN conda install --yes --name root pymongo
RUN ["bash", "-c", "source activate root && pip install rq-dashboard"] 
USER jovyan 


