
./dist/ccmanager: ./src/*
	./venv/bin/pyinstaller -F --name=ccmanager ./src/main.py

.PHONY: clean install

clean:
	rm -fr build *.spec dist
	find src -type d -name "__pycache__" -exec rm -fr {} +

install:
	cp ./dist/ccmanager /usr/local/bin/ccmanager
