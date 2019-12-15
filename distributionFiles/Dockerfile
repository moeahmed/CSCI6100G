# The container is based on the existing SciPy Notebook image
FROM jupyter/scipy-notebook

USER root

# Install OpenJDK (supports Clojure for Code-Maat)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-8-jdk \
    graphviz

# Install the required Python 2 packages
RUN conda create -n python2 python=2.7 psutil=4.1.0 notebook ipykernel pandas numpy matplotlib scikit-learn=0.19.0
RUN apt-get install -y python-pip


# Install Leiningen (used to run Code-Maat)
RUN mkdir -p /etc/pki/tls/certs
RUN ln -s /etc/ssl/certs/ca-certificates.crt /etc/pki/tls/certs/ca-bundle.crt

RUN wget -q -O /usr/bin/lein \
    https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein \
    && chmod +x /usr/bin/lein \
    && export PATH=$PATH:/usr/bin/

# Install Radon (a Python static metrics tool)
RUN pip install radon

# Return to the default user from jupyter/scipy-notebook
USER jovyan
RUN /bin/bash -c conda activate python2
RUN ipython kernel install --user
RUN python2 -m pip install pydot

