register:
	twine register

upload:
	python setup.py sdist
	twine upload --verbose dist/*
