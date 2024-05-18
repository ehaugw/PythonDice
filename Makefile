compileandexecute:
	@make -s tests
	@python3 simulations.py | column -t -s " " -o " "

tests:
	python3 dice.py
	python3 utilities.py

output:
	@python3 simulations.py | column -t -s " " -o " " > readme.md
