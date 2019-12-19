.PHONY: all clean install

all: install

install:
	sudo apt-get install tesseract-ocr
	wget https://github.com/tesseract-ocr/tessdata/raw/master/eng.traineddata # check the need for this
	sudo mv eng.traineddata /usr/share/tesseract-ocr/4.00/tessdata/eng.traineddata 

	python3 -m venv env

start:

end:

clean:
	rm -rf ./env/ ./.vscode/

info:
	pip freeze
