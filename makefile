all: seperate_data Vivino_wine_data.csv clean

seperate_data:
	python Vivino_web_scraper_Team10.py

Vivino_wine_data.csv: red_wine.csv white_wine.csv rose_wine.csv sparkling_wine.csv dessert_wine.csv fortified_wine.csv
	Rscript Data_Cleaning.R

clean:
	del red_wine.csv
	del white_wine.csv
	del rose_wine.csv
	del sparkling_wine.csv
	del dessert_wine.csv
	del fortified_wine.csv