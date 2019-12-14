# First build the image using the Dockerfile
# and name it 'toolkit' as follows:

# In the directory containing the Dockerfile:
# "docker build -t toolkit ."

# The script below runs the container
# Jupyter can be accessed in a web browser at 0.0.0.0:8888
docker run --rm -ti -v "$(pwd):/home/jovyan/work/" -p 8888:8888 \
toolkit  /bin/bash -c "source activate python2; jupyter notebook --no-browser"
