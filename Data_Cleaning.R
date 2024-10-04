## SETUP
#Install packages and import libraries
install.packages('readr')
library(readr)

## INPUT
# Import the data 
red_wine <- read_csv("red_wine.csv")
white_wine <- read_csv("white_wine.csv")
rose_wine <- read_csv("rose_wine.csv")
sparkling_wine <- read_csv("sparkling_wine.csv")
dessert_wine <- read_csv("dessert_wine.csv")
fortified_wine <- read_csv("fortified_wine.csv")

## TRANSFORMATION
# Add category that indicates the type of wine
red_wine$Category <- "Red"
white_wine$Category <- "White"
rose_wine$Category <- "Rosé"
sparkling_wine$Category <- "Sparkling"
dessert_wine$Category <- "Dessert"
fortified_wine$Category <- "Fortified"

# Merge seperate datasets to one big dataset
final_data <- rbind(red_wine, white_wine, rose_wine, sparkling_wine, dessert_wine, fortified_wine)

# Get hyperlink from each wine
hyperlink <- final_data$hyperlink

# Extract year of wine'
year <- sub(".*year=([0-9]+).*", "\\1", hyperlink)

# Set year as numeric so wines that do not show a year get NA
year = as.numeric(year)

# Add year as new variable in the data
final_data$Year <- year

# Extract the wine id from the Hyperlink
wine_id <- sub(".*/w/([0-9]+)\\?.*", "\\1", hyperlink)

# Change hyperlink to WineID
final_data$hyperlink <- wine_id
names(final_data)[1]<-paste("WineID")

# Rename Reviews to ReviewCount
names(final_data)[5]<-paste("ReviewCount")

# Wine rating is shown without comma, divide ratings by 10
final_data$Rating <- final_data$Rating / 10

# Change timestamp to readable date (YY-MM-DD)
final_data$Timestamp <- as.Date(as.POSIXct(final_data$Timestamp, origin="1970-01-01"))

# Since some wines are offered multiple times on the Vivino website, it is important to only keep unique wines so there are no duplicates
final_data <- unique(final_data)

## OUTPUT
write.csv(final_data, 'Vivino_wine_data.csv', row.names = FALSE)
