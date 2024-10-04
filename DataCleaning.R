## Code cleaning the data

#Install libraries and install packages

#load in the data

# before the for loop in python (can be deleted after automation of red & white wine)

# Red wines 

red_10 <- read_csv("red_wine_0_10.csv")
red_20 <- read_csv("red_wine_10_20.csv")
red_40 <- read_csv("red_wine_20_40.csv")
red_500 <- read_csv("red_wine_40_500.csv")

# White Wines

white_20 <- read_csv("white_wine_0_20.csv")
white_500 <- read_csv("white_wine_20_500.csv")

#Rosé wines

rose_wine <- read_csv("rose_wine.csv")

# Sparkling wines

sparkling_wines <- read_csv("sparkling_wines.csv")

# Dessert Wine
dessert_wine <- read_csv("dessert_wines.csv")

# Fortified wines

fortified_wines <- read_csv("fortified_wines.csv")

# After the for loop in python

red_wine <- read.csv("red_wine.csv")
white_wine <- read_csv("white_whine.csv")
rose_wine <- read_csv("rose_wine.csv")
sparkling_wines <- read_csv("sparkling_wines.csv")
dessert_wine <- read_csv("dessert_wines.csv")
fortified_wines <- read_csv("fortified_wines.csv")

# Add category


red_10$Category <- "Red"
red_20$Category <- "Red"
red_40$Category <- "Red"
red_500$Category <- "Red"

white_20$Category <- "White"
white_500$Category <- "White"

# If for loop is done in Python

red_wine$Category <- "Red"
white_wine$Category <- "White"
rose_wine$Category <- "Rosé"
sparkling_wines$Category <- "Sparkling"
dessert_wine$Category <- "Dessert"
fortified_wines$Category <- "Fortified"


# Attract the wine id from the Hyperlink

red_id <- red_wine$hyperlink
white_id <- white_wine$hyperlink
rose_id <- rose_wine$hyperlink
sparkling_id <- sparkling_wines$hyperlink
dessert_id <- dessert_wine$hyperlink
fortified_id <- fortified_wines$hyperlink

number_id_red <- sub(".*/w/([0-9]+)\\?.*", "\\1", red_id)
number_id_white <- sub(".*/w/([0-9]+)\\?.*", "\\1", white_id)
number_id_rose <- sub(".*/w/([0-9]+)\\?.*", "\\1", rose_id)
number_id_sparkling <- sub(".*/w/([0-9]+)\\?.*", "\\1", sparkling_id)
number_id_dessert <- sub(".*/w/([0-9]+)\\?.*", "\\1", dessert_id)
number_id_fortified <- sub(".*/w/([0-9]+)\\?.*", "\\1", fortified_id)

red_wine$WineID <- number_id_red
white_wine$WineID <- number_id_white
rose_wine$WineID <- number_id_rose
sparkling_wines$WineID <- number_id_sparkling
dessert_wine$WineID <- number_id_dessert
fortified_wines$WineID <- number_id_fortified

# Extract year of wine

red_year <- red_wine$hyperlink
white_year <- white_wine$hyperlink
rose_year <- rose_wine$hyperlink
sparkling_year <- sparkling_wines$hyperlink
dessert_year <- dessert_wine$hyperlink
fortified_year <- fortified_wines$hyperlink

red_year <- sub(".*year=([0-9]+).*", "\\1", red_year)
white_year <- sub(".*year=([0-9]+).*", "\\1", white_year)
rose_year <- sub(".*year=([0-9]+).*", "\\1", rose_year)
sparkling_year <- sub(".*year=([0-9]+).*", "\\1", sparkling_year)
dessert_year <- sub(".*year=([0-9]+).*", "\\1", dessert_year)
fortified_year <- sub(".*year=([0-9]+).*", "\\1", fortified_year)

red_wine$Year <- red_year
white_wine$Year <- white_year
rose_wine$Year <- rose_year
sparkling_wines$Year <- sparkling_year
dessert_wine$Year <- dessert_year
fortified_wines$Year <- fortified_year

####################

red_price <- red_wine$hyperlink
white_price <- white_wine$hyperlink
rose_price <- rose_wine$hyperlink
sparkling_price <- sparkling_wines$hyperlink
dessert_price <- dessert_wine$hyperlink
fortified_price <- fortified_wines$hyperlink


red_id_price <- sub(".*price_id=([0-9]+).*", "\\1", red_price)
white_id_price <- sub(".*price_id=([0-9]+).*", "\\1", white_price)
rose_id_price <- sub(".*price_id=([0-9]+).*", "\\1", rose_price)
sparkling_id_price <- sub(".*price_id=([0-9]+).*", "\\1", sparkling_price)
dessert_id_price <- sub(".*price_id=([0-9]+).*", "\\1", dessert_price)
fortified_id_price <- sub(".*price_id=([0-9]+).*", "\\1", fortified_price)


sparkling_wines$PriceID <- sparkling_id_price


