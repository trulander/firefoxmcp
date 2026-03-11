FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:1
ENV HOME=/root

RUN apt-get update && apt-get install -y \
    software-properties-common \
    curl \
    ca-certificates \
    git \
    && add-apt-repository -y ppa:mozillateam/ppa \
    && echo 'Package: *\nPin: release o=LP-PPA-mozillateam\nPin-Priority: 1001' > /etc/apt/preferences.d/mozilla-ppa \
    && apt-get update && apt-get install -y \
    firefox-esr \
    xvfb \
    x11vnc \
    websockify \
    supervisor \
    openbox \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Install noVNC manually from GitHub
RUN git clone https://github.com/novnc/noVNC.git /opt/noVNC \
    && git clone https://github.com/novnc/websockify.git /opt/noVNC/utils/websockify

# Download FoxMCP xpi from the latest GitHub release
RUN curl -L "https://github.com/ThinkerYzu/foxmcp/releases/download/v1.1.0/foxmcp@codemud.org.xpi" \
    -o /opt/foxmcp.xpi

# Configure Firefox: disable signature check, set ws server
COPY autoconfig.js /usr/lib/firefox-esr/defaults/pref/autoconfig.js
COPY firefox.cfg /usr/lib/firefox-esr/firefox.cfg

COPY install-foxmcp.sh /opt/install-foxmcp.sh
RUN chmod +x /opt/install-foxmcp.sh

COPY supervisord.conf /etc/supervisord.conf

EXPOSE 6080

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf", "-n"]
