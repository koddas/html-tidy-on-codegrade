# Running HTML Tidy on CodeGrade
A simple wrapper for running HTML Tidy on CodeGrade.

[HTML Tidy](https://www.html-tidy.org/) is a nifty little application that cleans HTML files. It also outputs info on what it changes, which makes it possible to use the tool as an HTML code quality checker.

## Installing and running on CodeGrade

Simply upload the files (*setup.sh*, *install-tidy.sh*, *tidy.py*, and *config.txt*) as fixtures. Set *Global setup script* to *$FIXTURES/setup.sh*. Then, under your auto test, add a **Code Quality** block. Choose a **custom** linter and set *Custom program* to *$FIXTURES/tidy.py* and set up deduction scores as you wish. HTML Tidy will only output errors and warnings, but is pretty lax with what it considers to be an error (I would've been far less lenient when grading myself), and treats most errors as warnings.

The tool will check all submitted HTML files, as long as the students don't submit anything in subdirectories. There is also a config file, *config.txt*, which you can tweak. You'll find its [documentation here](http://api.html-tidy.org/tidy/quickref_5.0.0.html).

## Examples

There are two example files that you can use to test your setup. You'll find them under [examples](examples). The first one, *[good.html](examples/good.html)*, shouldn't contain any faults and won't trigger any response from the tool. The second one, *[bad.html](examples/bad.html)*, is rife with errors and will trigger at least five warnings for you to examine.