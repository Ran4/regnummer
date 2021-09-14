run:
	@. .venv/bin/activate && python3 regnummer.py MSZ541

install:
	python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
