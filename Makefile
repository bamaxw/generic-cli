version = `cat ./VERSION`
package-name = generic-cli


test:
	echo "no tests"
	# python -m green -ar tests/*.py

upload: test vpatch
	devpi upload
	rm -r dist

example:
	pipenv run python example.py

install-locally:
	pip install -U .

publish:
	devpi push "$(package-name)==$(version)" "inyourarea/prod"

vpatch:
	bumpversion patch

vminor:
	bumpversion minor

vmajor:
	bumpversion major
