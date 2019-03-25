register:
	python setup.py register -r pypi

upload:
	twine upload dist/*
