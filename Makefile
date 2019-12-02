include flags-env.mk

.PHONY: all clean install

all: install

install:
ifdef INSTALL_PACKAGES
	sudo apt-get install python3-pip
	pip3 install virtualenv

	sudo apt-get install tesseract-ocr
	wget https://github.com/tesseract-ocr/tessdata/raw/master/eng.traineddata # check the need for this
	mv eng.traineddata /usr/share/tesseract-ocr/4.00/tessdata/eng.traineddata 
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
	rm -rf ./env/ ./.vscode/

info:
	pip freeze
