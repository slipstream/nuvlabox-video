FROM ubuntu:18.04

#ADD pre-install.sh /root/pre-install.sh
#RUN chmod a+x /root/pre-install.sh

#RUN /root/pre-install.sh 

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update -q \
    && apt-get install -y --no-install-recommends \
       -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confnew" \
       g++ git libsm-dev \
       python3-opencv python3-numpy \
       python3-flask python3-pip \
       usbutils wget \
    && apt-get clean \
    && apt-get autoremove -y

ADD post-install.sh /root/post-install.sh
RUN chmod a+x /root/post-install.sh
ADD deployment.sh /root/deployment.sh
RUN chmod a+x /root/deployment.sh

RUN /root/post-install.sh

CMD ["/bin/bash"]
