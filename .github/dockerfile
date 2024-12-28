FROM fedora:42@sha256:70d5934128fe1b1abc97750dc358dad9cf499c11059f0ed720872fedcc4880d1

# Define variables
ARG USERNAME=actions
ARG USER_HOME=/home/$USERNAME

# Upgrade all packages
RUN dnf -y upgrade --refresh

RUN dnf -y install curl wget sudo python-copr python-copr-doc \ 
  dnf-plugins-core git && dnf clean all

RUN useradd -m -d $USER_HOME $USERNAME && \
  usermod -aG wheel $USERNAME && \
  echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Set the default user
USER $USERNAME

# Set the HOME environment variable
ENV HOME=$USER_HOME

# Set the working directory to the home directory
WORKDIR $USER_HOME

# Set bash as the default shell
ENTRYPOINT ["/bin/bash"]
