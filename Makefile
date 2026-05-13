# ─── Makefile ────────────────────────────────────────────────────────────────
MAIN    = main
LATEXMK = latexmk
FLAGS   = -pdf -bibtex -interaction=nonstopmode -shell-escape

.PHONY: all clean distclean watch

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex referencias.bib
	$(LATEXMK) $(FLAGS) $(MAIN)

watch:
	$(LATEXMK) $(FLAGS) -pvc $(MAIN)

clean:
	$(LATEXMK) -c $(MAIN)
	rm -f *.aux *.bbl *.bcf *.blg *.log *.out *.run.xml *.toc *.fls *.fdb_latexmk

distclean: clean
	rm -f $(MAIN).pdf
