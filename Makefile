clean:
	python dev/clean.py

deps:
	pip install -r requirements.txt --upgrade

deploy: clean pypi
	git push --tags
	twine upload -r pypi dist/*
	python dev/clean.py

pypi: clean
	python setup.py sdist bdist_wheel

pypi-test:
	python setup.py sdist upload -r pypitest

register:
	python setup.py register -r pypi

register-test:
	python setup.py register -r pypitest