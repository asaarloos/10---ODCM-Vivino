all: seperate_data ../../data/Vivino_wine_data.csv clean

seperate_data:
	python Vivino_web_scraper_Team10.py

../../data/Vivino_wine_data.csv: ../../data/red_wine.csv ../../data/white_wine.csv ../../data/rose_wine.csv ../../data/sparkling_wine.csv ../../data/dessert_wine.csv ../../data/fortified_wine.csv
	Rscript ../reporting/Data_Cleaning.R

clean:
	del ../../data/red_wine.csv
	del ../../data/white_wine.csv
	del ../../data/rose_wine.csv
	del ../../data/sparkling_wine.csv
	del ../../data/dessert_wine.csv
	del ../../data/fortified_wine.csv