.PHONY: all clean

all: main.pdf

main.pdf: main.tex preamble.tex references.bib $(wildcard sections/*.tex)
	pdflatex main.tex
	bibtex main
	pdflatex main.tex
	pdflatex main.tex

clean:
	rm -f main.aux main.bbl main.blg main.log main.out main.pdf main.toc main.fdb_latexmk main.fls main.synctex.gz
