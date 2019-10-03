FROM python:3.7

WORKDIR /root
ENTRYPOINT ["/bin/bash"]

RUN TERM=dumb \
	apt update -y && \
	apt upgrade -y && \
	apt install -qy --no-install-recommends \
	apt-utils \
	ffmpeg \
	sox \
	libcairo2-dev \
	texlive \
	texlive-fonts-extra \
	texlive-latex-extra \
	texlive-latex-recommended \
	texlive-science \
	texlive-xetex \
	texlive-lang-chinese \
	texlive-generic-recommended \
	tipa \
	&& \
	rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/3b1b/manim /manim

COPY manimlib/ /manim/manimlib/

RUN cd /manim \
	&& git checkout 0.1.10 \
	&& sed -i 's/TEX_USE_CTEX = False/TEX_USE_CTEX = True/g' /manim/manimlib/constants.py \
	&& sed -i 's/microtype}/microtype}\\usepackage{fontspec}\\setmainfont{ISOCPEUR}/g' /manim/manimlib/ctex_template.tex \
	&& python setup.py sdist \
	&& python -m pip install dist/manimlib*

COPY fonts/* /usr/share/fonts/truetype/
