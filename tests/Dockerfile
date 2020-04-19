FROM ubuntu:18.04

# apt-get and system utilities
RUN apt-get update && apt-get install -y \
    curl apt-utils apt-transport-https debconf-utils gcc build-essential g++-5 \
    && rm -rf /var/lib/apt/lists/*

# Install SQL Server drivers and tools
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && ACCEPT_EULA=Y apt-get install -y mssql-tools \
    && apt-get install -y unixodbc-dev libssl1.0.0 \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/opt/mssql-tools/bin:${PATH}"

# Python 3 libraries
RUN apt-get update \
    && apt-get install -y python3-pip python3-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

# Install necessary locales
RUN apt-get update && apt-get install -y locales \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen \
    && rm -rf /var/lib/apt/lists/*

# Install development and debugging tools that are not required for the app to function
# You can remove them safely from your application as long as you do not use them in the code
RUN apt-get update && apt-get install -y vim dnsutils \
	&& pip install ipython \
    && rm -rf /var/lib/apt/lists/*

ARG USER=bcpyer
RUN groupadd -r --gid 1000 ${USER} \
    && useradd --create-home --uid 1000 ${USER} -r -g ${USER}

USER ${USER}
ENV PATH="/home/${USER}/.local/bin:${PATH}"

COPY --chown=1000:1000 ./requirements.txt /bcpy/requirements.txt
RUN pip install -r /bcpy/requirements.txt

COPY --chown=1000:1000 ./ /bcpy/
WORKDIR /bcpy
RUN pip install -e .
