DATA = ../../data

all: $(DATA)/Vivino_wine_data.csv clean

separate_data: Vivino_web_scraper_Team10.py
	python Vivino_web_scraper_Team10.py

$(DATA)/Vivino_wine_data.csv: separate_data Data_Cleaning.R 
	Rscript Data_Cleaning.R

clean:
	del $(DATA)/red_wine.csv
	del $(DATA)/white_wine.csv
	del $(DATA)/rose_wine.csv
	del $(DATA)/sparkling_wine.csv
	del $(DATA)/dessert_wine.csv
	del $(DATA)/fortified_wine.csv 