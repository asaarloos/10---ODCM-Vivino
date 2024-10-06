# Team Project ODCM - Team 10

## Project 
In this project, we scrape date from the website Vivino. The extracted data could be used to analyse the influence of the price of wine on consumer ratings. The Vivino website offers over millions of different wines, it is impossible to scrape all of them. Therefore, we made created a sample of wines we are going to scrape. This sample consists of all wines originated in Spain and that is deliverable to the Netherlands. As of 05-10-2024 This leaves a sample of 7,585 wines (this number could change over time). Of these wines, the following data will be extracted:
- **Hyperlink**: The hyperlink of each wine, which includes the unique id of each wine. The unique wine id will later be isolated when cleaning the data.
- **Brand**: The brand that produces the wine.
- **Wine**: The name of the specific wine.
- **Rating**: The star rating of the specific wine (0-5).
- **Reviews**: The number of reviews a specific wine has.
- **Price**: The price of the specific wine. When the wine is on discount, the original price will be taken, not the discounted price.
- **Timestamp**: The timestamp at which the data is extracted. This is useful if the dataset will be used in future analysis, so the date and time of extraction can always be found.

*Note: Since the Vivino website offerse some wines multiple times, later the duplicate rows will be deleted, which leaves a sample of 7,618 wines*

## Code
When the makefile is run in the terminal, the code will automatically run. This consists of 3 parts:

### 1. Webscraping
First ther webscraping code will run, which can be found in the 'Vivino-web-scraper-Team10' file. The code will run individually for each type of wine: red, white, rose, sparkling, dessert and fortified. After the code of each type is run, a dataset will be created containing all wines of that type (so 6 datasets in total). Later, when cleaning the data, each dataset will get identified by adding an extra column with the type. Then, all datasets will be merged into one dataset containing all 8,057 wines. This dataset will be further cleaned and after removing duplicate wines, it will producte a final dataset with 7,585 wines.

### 2. Cleaning
When all 6 seperate datasets are created, a Rscript will run which cleans this data. This code can be found in the 'Data_Cleaning' file. First, for each dataset a column will be added, incidcating the type of wine. Then all 6 datasets will be merged to one final dataset named 'Vivino-wine-data'. This data will be further cleaned. Since Vivino offers some wines multiple times on the website, all duplicate rows are removed. The final data will be stored in a csv file (Vivino-wine-data.csv), containing information of 7,585 wines.

### 3. Removing Irrelevant Files
When all the code has run, the 6 datasets that are created by the webscraper (before merging) will automatically be removed. Since all information can also be found in the final dataset, these seperate datasets are of no use anymore. In order to keep a tidy workspace, the old datafiles are removed.

Running the code takes approximate 45 minutes. **When the code is running, do not interupt, so the code does not break!**

## Important note
Make sure that, before running the makefile, the following python packages are installed:
```
!pip3 install selenium
!pip3 install webdriver_manager
!pip3 install beautifulsoup4
