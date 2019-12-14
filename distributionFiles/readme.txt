Software Metrics Research Toolkit and Data distribution package

To support the M.A.Sc. thesis "Toolkit for Automatic Collection and Predictive Modelling of Software Metrics"

Maintained by: Tim Johnston (johnst3@mcmaster.ca)
Updated 20 June 2016


To install and run:

1) Install Docker and build the Docker container (see i. below)
2) Run the container with the provided script (see ii. below)
3) Access the Jupyter notebook server at 0.0.0.0:8888 in a web browser
4) Navigate to toolkit/ and run 'caseStudy.ipynb' or 'repeatStudies.ipynb'



Contents:

i. Dockerfile

    This can be used to build the Docker container.
    In the directory containing the Dockerfile:
        "docker build -t toolkit ."

    This requires Docker to be installed, with the Docker daemon running.
    All components other than Docker are provided by the resulting container.

    For instructions to install Docker, see:
    https://docs.docker.com/linux/step_one/
    https://docs.docker.com/mac/step_one/

ii. runContainer.sh

    This can be used to run the Docker container after it has been built.
    This creates a Jupyter notebook server, which
    can be accessed at 0.0.0.0:8888 in a web browser.

iii. datasets/

    Contains populated metrics databases for the 5
    studied projects (git, Vim, OpenSSL, httpd, nginx).

    When running the case study notebooks, this directory will
    be populated with extra data from git repositories,
    and decision tree visualization diagrams.

iv. toolkit/

    This contains the toolkit source code, and Jupyter
    notebooks for the case study. To repeat the case study,
    open 'caseStudy.ipynb' or 'repeatStudies.ipynb' in
    Jupyter and run all the code cells.

v. code-maat/

    A precompiled copy of the Code-Maat tool.
    This is provided rather than building from
    the source code, to avoid setup issues with
    Java/OpenJDK and Leiningen.

    Code-Maat can be found on Github at:
    https://github.com/adamtornhill/code-maat

vi. cqmetrics/

    A precompiled copy of cqmetrics is provided as well.

    cqmetrics can be found on Github at:
    https://github.com/dspinellis/cqmetrics
