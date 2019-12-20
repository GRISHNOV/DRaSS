.PHONY: all install start end clean info

all: install

install:
	sudo apt install tesseract-ocr
	wget https://github.com/tesseract-ocr/tessdata/raw/master/eng.traineddata
	sudo mv eng.traineddata /usr/share/tesseract-ocr/4.00/tessdata/eng.traineddata

	sudo apt install xterm 

	python3 -m venv env

start:
	# cd src && python3 run.py
	python3 src/run.py

end:

clean:
	rm -rf ./env/ ./.vscode/

uninstall: clean
	sudo apt remove tesseract-ocr
	sudo apt remove xterm 

info:
	pip freeze
