# Load necessary libraries
library(tidyverse)
library(ggplot2)
library(knitr)
library(kableExtra)

# Load the dataset 
wine_data <- read.csv("Vivino_wine_data.csv")

# Summary statistics
summary_stats <- wine_data %>%
  summarise(
    Mean_Rating = mean(Rating, na.rm = TRUE),
    SD_Rating = sd(Rating, na.rm = TRUE),
    Mean_ReviewCount = mean(ReviewCount, na.rm = TRUE),
    SD_ReviewCount = sd(ReviewCount, na.rm = TRUE),
    Mean_Price = mean(Price, na.rm = TRUE),
    SD_Price = sd(Price, na.rm = TRUE)
  )

# Display summary statistics
summary_stats_table <- kable(summary_stats, digits = 2, caption = "Summary Statistics for Continuous Variables") %>%
  kable_styling(full_width = FALSE)
print(summary_stats_table)

# Frequency distribution for Brand
brand_distribution <- wine_data %>%
  group_by(Brand) %>%
  summarise(Frequency = n()) %>%
  arrange(desc(Frequency))

# Display frequency distribution
brand_table <- kable(brand_distribution, caption = "Frequency Distribution of Wine Brands") %>%
  kable_styling(full_width = FALSE)

print(brand_table)

# Count unique brands
unique_brands_count <- wine_data %>%
  summarise(Unique_Brands = n_distinct(Brand))
print(unique_brands_count)

# Histogram for Rating
ggplot(wine_data, aes(x = Rating)) +
  geom_histogram(binwidth = 0.5, fill = "blue", color = "black", alpha = 0.7) +
  labs(title = "Distribution of Wine Ratings", x = "Rating", y = "Count") +
  theme_minimal()

# Histogram of Year
ggplot(wine_data, aes(x = Year)) +
  geom_histogram(binwidth = 1, fill = 'lightblue', color = 'black') +
  labs(title = "Histogram of Wine Harvest Years", x = "Year", y = "Count") +
  theme_minimal()

# Create scatter plot with log transformation of Price
ggplot(data = wine_data, aes(x = log(Price), y = Rating)) +
  geom_point(color = "blue", size = 2) + 
  geom_smooth(method = "lm", se = FALSE, color = "red") + 
  labs(title = "Price vs Rating of Wines (Log-Transformed Price)",
       x = "Log of Price (Euro)",
       y = "Rating (0-5)") +
  ylim(0, 5) +  
  theme_minimal()  
