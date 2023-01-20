.PHONY: test, example1, example2, executable

test:
	python3 -m pytest tests/tests.py

example1:
	python3 src/most_active_cookie.py logfiles/cookies.txt -d 2018-12-09

example2:
	python3 src/most_active_cookie.py logfiles/cookies.txt -d 2018-12-0

example3:
	./src/most_active_cookie.py logfiles/cookies.txt -d 2018-12-09

clean:
	rm -f logfiles/tests_basic.csv logfiles/tests_multiple.csv

