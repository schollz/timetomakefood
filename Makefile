install:
	( \
		virtualenv -p /usr/bin/python3 venv; \
		venv/bin/pip install -Ur requirements.txt; \
	)
	@echo "\n\nTo run use:"
	@echo " source venv/bin/activate"
	@echo "(venv) python parser.py\n\n"
	
clean:
	rm -rf venv/
	rm -rf __pycache__/