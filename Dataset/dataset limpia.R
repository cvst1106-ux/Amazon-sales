#Cargar librerías
library(tidyverse)
library(knitr)
library(kableExtra)
library(scales)
library(janitor)

#Carga del archivo
df <- read.csv("11. Amazon Sales.csv", encoding = "UTF-8")

#Limpieza completa
df_limpio <- df %>%
  janitor::clean_names() %>%
  select(product_id, product_name, category, actual_price, discount_percentage, discounted_price) %>%
  mutate(
    actual_price = as.numeric(gsub("[^0-9.]", "", actual_price)),
    discounted_price = as.numeric(gsub("[^0-9.]", "", discounted_price )),
    discount_percentage = as.numeric(gsub("[^0-9.]", "", discount_percentage)) / 100
  )

#Recalculo de %
df_limpio <- df_limpio %>%
  mutate(
    discounted_price = actual_price - (actual_price * discount_percentage),
    discounted_price = round(discounted_price, 0)
  )

#Cálculo de outliers
Q1 <- quantile(df_limpio$actual_price, 0.25, na.rm = TRUE)
Q3 <- quantile(df_limpio$actual_price, 0.75, na.rm = TRUE)
IQR_val <- Q3 - Q1

limite_inferior <- Q1 - 1.5 * IQR_val
limite_superior <- Q3 + 1.5 * IQR_val

#Filtrado final y quitar null, na
df_sin_atipicos <- df_limpio %>%
  filter(actual_price >= limite_inferior & actual_price <= limite_superior)
is.na.data.frame("Amazon SAles.11.csv") 
colSums(is.na(df_limpio[, c("actual_price", "discount_percentage", "discounted_price")]))
