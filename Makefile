LATEST_VERS='0.5'

dist/ssmp-$(LATEST_VERS).tar.gz:
	python ./setup.py sdist

build: dist/ssmp-$(LATEST_VERS).tar.gz

PHONY: install
	python ./setup.py install

PHONY: clean
clean:
	find . -name '*.pyc' | xargs rm
	rm -fr build MANIFEST dist
