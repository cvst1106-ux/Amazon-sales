# Cargar librerías necesarias
library(tidyverse)
library(knitr)
library(kableExtra)
library(scales)
library(janitor)

# 1. Carga del archivo
df <- read.csv("11. Amazon Sales.csv", encoding = "UTF-8")

# 1. Limpieza inicial incluyendo TODAS las columnas necesarias
df_limpio <- df %>%
  janitor::clean_names() %>%
  # ¡IMPORTANTE! Añadimos discount_percentage aquí:
  select(product_id, product_name, category, actual_price, discount_percentage, discounted_price) %>%
  mutate(
    # Limpiamos los precios (quitar rupias y comas)
    actual_price = as.numeric(gsub("[^0-9.]", "", actual_price)),
    discounted_price = as.numeric(gsub("[^0-9.]", "", discounted_price )),
    # Limpiamos el porcentaje si tiene el símbolo % (ej: "10%" -> 0.10)
    discount_percentage = as.numeric(gsub("[^0-9.]", "", discount_percentage)) / 100
  )

# 2. Recalculo de precios
df_limpio <- df_limpio %>%
  mutate(
    discounted_price = actual_price - (actual_price * discount_percentage),
    discounted_price = round(discounted_price, 0)
  )

# 3. Verificación
head(df_limpio)

# 3. CÁLCULO DE OUTLIERS (Ahora sí funcionará porque son números)
Q1 <- quantile(df_limpio$actual_price, 0.25, na.rm = TRUE)
Q3 <- quantile(df_limpio$actual_price, 0.75, na.rm = TRUE)
IQR_val <- Q3 - Q1

limite_inferior <- Q1 - 1.5 * IQR_val
limite_superior <- Q3 + 1.5 * IQR_val

# 4. FILTRADO FINAL
df_sin_atipicos <- df_limpio %>%
  filter(actual_price >= limite_inferior & actual_price <= limite_superior)

# 5. VERIFICACIÓN
nrow(df_sin_atipicos)
summary(df_sin_atipicos$actual_price)
