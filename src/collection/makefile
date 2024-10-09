DATA = ../../data

all: seperate_data $(DATA)/Vivino_wine_data.csv clean

seperate_data: Vivino_web_scraper_Team10.py
	python Vivino_web_scraper_Team10.py

$(DATA)/Vivino_wine_data.csv: $(DATA)/red_wine.csv $(DATA)/white_wine.csv $(DATA)/rose_wine.csv $(DATA)/sparkling_wine.csv $(DATA)/dessert_wine.csv $(DATA)/fortified_wine.csv Data_Cleaning.R
	Rscript Data_Cleaning.R

clean:
	del $(DATA)/red_wine.csv
	del $(DATA)/white_wine.csv
	del $(DATA)/rose_wine.csv
	del $(DATA)/sparkling_wine.csv
	del $(DATA)/dessert_wine.csv
	del $(DATA)/fortified_wine.csv 