FROM itamtao/nltk

MAINTAINER Tao Lin <itamtao@gmail.com>

USER root

RUN mkdir t && cd t && wget http://snap.stanford.edu/snappy/release/snap-1.2-2.4-centos6.5-x64-py2.6.tar.gz && \
    tar zxvf snap-1.2-2.4-centos6.5-x64-py2.6.tar.gz && \
    cd snap-1.2-2.4-centos6.5-x64-py2.6 && \
    python setup.py install


# install gnuplot for plotting structural properties of networks (e.g., degree distribution);
RUN apt-get update && apt-get install -y gnuplot

# install Graphviz for drawing and visualizing small graphs.
# RUN apt-get -y remove libpathplan4 libgraphviz4 libxdot4 libcgraph6 libcdt5
# RUN apt-get -y install libatk1.0-0 libgtk2.0-0 libgts-0.7-5 liblasi0
# RUN wget http://www.graphviz.org/pub/graphviz/stable/ubuntu/ub13.10/x86_64/libgraphviz4_2.38.0-1~saucy_amd64.deb && \
#     dpkg -i libgraphviz4_2.38.0-1~saucy_amd64.deb
#
# RUN apt-get -y install freeglut3 libgl1-mesa-glx libgl1 libglade2-0 libglu1-mesa libglu1 libgtkglext1
# RUN wget http://www.graphviz.org/pub/graphviz/stable/ubuntu/ub13.10/x86_64/graphviz_2.38.0-1~saucy_amd64.deb && \
#     dpkg -i graphviz_2.38.0-1~saucy_amd64.deb

# RUN pip install --no-cache graphviz

RUN rm -rf t



USER tlin
