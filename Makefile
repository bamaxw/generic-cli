version = `cat ./VERSION`
package-name = generic-cli


test:
	echo "no tests"
	# python -m green -ar tests/*.py

upload: test vpatch
	devpi upload
	rm -r dist

install-locally:
	pip install -U .

publish:
	devpi push "$(package-name)==$(version)" "ai-unit/prod"

vpatch:
	bumpversion patch

vminor:
	bumpversion minor

vmajor:
	bumpversion major
