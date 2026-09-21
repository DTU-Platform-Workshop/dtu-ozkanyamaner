# This first line lets you build on top of an existing Docker image
# You can build on top of any image you'd like, the image you create 
# here can be used to be built on top of as well
FROM python:3.12-slim

# Setup environment variables to improve the performance of our Python 
# application
ENV PYTHONUNBUFFERED=1 \
    PORT=4242 \
    # Read-only root FS at runtime: keep any home/temp writes on the /tmp mount.
    HOME=/tmp \
    TMPDIR=/tmp

# The second line here sets the "working directory" inside the Docker 
# image.
WORKDIR /app

# Because Containers use a lot of caching, it's always best to put the things
# that change most often at the end and least often at the top.
# So we can improve our build times significantly by installing our 
# dependencies before our source code.
COPY requirements.txt ./

# With the RUN keyword you can run commands inside the image
# This is typically just regular bash commands
RUN pip install --no-cache-dir -r requirements.txt

# You can copy specific files or even whole directories into the Docker
# image. If you want to copy all of the current directory into the 
# Docker image, you can write:
# COPY . /app/
# You can also just copy the files you need:
COPY app.py /app/

# Run as non-root (numeric UID; no user entry needed for read-only FS).
USER 10001

# The EXPOSE doesn't actually do anything, it just adds information 
# about which port this Docker image uses
EXPOSE 4242

# Set the entrypoint in the Docker image, in Docker containers the 
# command that is run split into "entrypoint" and "command" 
# Where "entrypoint" is the program to run and "command" is the 
# arguments for the program. 
ENTRYPOINT ["python"]

# This will ask Python to run the app.py file
CMD ["app.py"]
