.PHONY: clean install

./dist/ccmanager: .venv.timestamp ./src/*.py
	./venv/bin/pyinstaller -F --name=ccmanager ./src/main.py

.venv.timestamp: requirements.txt
	python -m venv venv
	./venv/bin/pip install -r requirements.txt
	@touch .venv.timestamp

clean:
	rm -fr build *.spec dist venv .venv.timestamp
	find src -type d -name "__pycache__" -exec rm -fr {} +

install:
	cp ./dist/ccmanager /usr/local/bin/ccmanager
