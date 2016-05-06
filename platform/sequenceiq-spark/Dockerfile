FROM sequenceiq/hadoop-docker:2.6.0
MAINTAINER SequenceIQ

ENV HADOOP_VERSION 2.6
ENV SPARK_VERSION 1.6.1
ENV SCALA_VERSION 2.11.7
ENV SBT_VERSION 0.13.11

#support for Hadoop 2.6.0
RUN curl -s http://d3kbcqa49mib13.cloudfront.net/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz | tar -xz -C /usr/local/
RUN cd /usr/local && ln -s spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION spark
ENV SPARK_HOME /usr/local/spark
RUN mkdir $SPARK_HOME/yarn-remote-client
ADD yarn-remote-client $SPARK_HOME/yarn-remote-client

RUN $BOOTSTRAP && $HADOOP_PREFIX/bin/hadoop dfsadmin -safemode leave && $HADOOP_PREFIX/bin/hdfs dfs -put $SPARK_HOME-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION/lib /spark

ENV YARN_CONF_DIR $HADOOP_PREFIX/etc/hadoop
ENV PATH $PATH:$SPARK_HOME/bin:$HADOOP_PREFIX/bin
# update boot script
COPY bootstrap.sh /etc/bootstrap.sh
RUN chown root.root /etc/bootstrap.sh
RUN chmod 700 /etc/bootstrap.sh

#install R
RUN rpm -ivh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
RUN yum -y install R

# install scala
RUN curl -o /usr/local/scala-2.11.8.tgz http://www.scala-lang.org/files/archive/scala-2.11.8.tgz
RUN tar zxf /usr/local/scala-2.11.8.tgz -C /usr/local/
RUN ln -s /usr/local/scala-2.11.8 /usr/local/share/scala
RUN ln -s /usr/local/share/scala/bin/scala /usr/bin/scala
RUN ln -s /usr/local/share/scala/bin/scalac /usr/bin/scalac
RUN ln -s /usr/local/share/scala/bin/fsc /usr/bin/fsc
RUN ln -s /usr/local/share/scala/bin/sbaz /usr/bin/sbaz
RUN ln -s /usr/local/share/scala/bin/sbaz-setup /usr/bin/sbaz-setup
RUN ln -s /usr/local/share/scala/bin/scaladoc /usr/bin/scaladoc
RUN ln -s /usr/local/share/scala/bin/scalap /usr/bin/scalap

# install sbt
RUN curl https://bintray.com/sbt/rpm/rpm > bintray-sbt-rpm.repo
RUN mv bintray-sbt-rpm.repo /etc/yum.repos.d/
RUN yum -y install sbt

# install java 1.7.0
RUN yum -y install java-1.7.0-openjdk*

# install git
RUN yum -y update
RUN yum -y install git

# install zsh
RUN git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh \
      && cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc

ENTRYPOINT ["/etc/bootstrap.sh"]
