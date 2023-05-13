options(width = 200)

csv_path <- commandArgs(trailingOnly = TRUE)[1]

df <- read.csv(csv_path, header = TRUE, sep = ";")

model <- lm(NPOPCHG2022 ~ ., data = df)

summary(model)
