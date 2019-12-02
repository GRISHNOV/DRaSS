include flags-env.mk

.PHONY: all clean install

all: install

install:
ifdef INSTALL_PACKAGES
	sudo apt-get install python3-pip
	pip3 install virtualenv
endif

ifdef INSTALL_ENV
	python3 -m venv env
	pip3 install -r requirements.txt
endif

start:
	source ./env/bin/activate

end:
	deactivate

clean:
	rm -r ./env

info:
	pip freeze
