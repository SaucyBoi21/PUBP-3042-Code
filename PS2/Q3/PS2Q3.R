#literacy and education are postive, poverty is negative
library(dplyr)
library(lmtest)
library(ggplot2)

data <- read.csv("./PS2/Q3/transfer.csv")
#View(data)

cutoff1 <- 10188
cutoff2 <- 13584
cutoff3 <- 16980

midpoint1 <- (cutoff1 + cutoff2) / 2
midpoint2 <- (cutoff2 + cutoff3) / 2

population <- data$pop82
data$normalized_pscore <- NA
count <- 1

for (value in population) {

    if (value <= midpoint1) {
        diff <- (value - cutoff1) / cutoff1 * 100
    }
    else if (value <= midpoint2) {
        diff <- (value - cutoff2) / cutoff2 * 100
    }
    else {
        diff <- (value - cutoff3) / cutoff3 * 100
    }

    data$normalized_pscore[count] <- diff
    count <- count + 1

}

pscore <- data$normalized_pscore

subset <- filter(data, pscore >= -3 & pscore <= 3)
subset.below <- filter(data, pscore >= -3, pscore < 0)
subset.above <- filter(data, pscore <= 3, pscore >= 0)

#View(subset)

lit91 <- subset$literate91
lit91.fit.below <- lm(literate91 ~ normalized_pscore, data = subset.below)
lit91.fit.above <- lm(literate91 ~ normalized_pscore, data = subset.above)

lit91_effect <- coef(lit91.fit.above)[1] - coef(lit91.fit.below)[1]
print(lit91_effect)

lit_graph <- ggplot() +
    geom_point(data = subset, aes(x = normalized_pscore, y = literate91)) +
    geom_smooth(data = subset.below, aes(x = normalized_pscore, y = literate91), method = "lm", color = "blue", se=FALSE) +
    geom_smooth(data = subset.above, aes(x = normalized_pscore, y = literate91), method = "lm", color = "red", se=FALSE)


ggsave("lit_plot.png", plot = lit_graph, width = 6, height = 4, dpi = 300)

educ91 <- subset$educ91
educ91.fit.below <- lm(educ91 ~ normalized_pscore, data = subset.below)
educ91.fit.above <- lm(educ91 ~ normalized_pscore, data = subset.above)

educ91_effect <- coef(educ91.fit.above)[1] - coef(educ91.fit.below)[1]
print(educ91_effect)

educ_graph <- ggplot() +
    geom_point(data = subset, aes(x = normalized_pscore, y = literate91)) +
    geom_smooth(data = subset.below, aes(x = normalized_pscore, y = literate91), method = "lm", color = "blue", se=FALSE) +
    geom_smooth(data = subset.above, aes(x = normalized_pscore, y = literate91), method = "lm", color = "red", se=FALSE)


ggsave("educ_plot.png", plot = educ_graph, width = 6, height = 4, dpi = 300)

pov91 <- subset$poverty91
pov91.fit.below <- lm(poverty91 ~ normalized_pscore, data = subset.below)
pov91.fit.above <- lm(poverty91 ~ normalized_pscore, data = subset.above)

pov91_effect <- coef(pov91.fit.above)[1] - coef(pov91.fit.below)[1]
print(pov91_effect)

pov_graph <- ggplot() +
    geom_point(data = subset, aes(x = normalized_pscore, y = poverty91)) +
    geom_smooth(data = subset.below, aes(x = normalized_pscore, y = poverty91), method = "lm", color = "blue", se=FALSE) +
    geom_smooth(data = subset.above, aes(x = normalized_pscore, y = poverty91), method = "lm", color = "red", se=FALSE)


ggsave("pov_plot.png", plot = pov_graph, width = 6, height = 4, dpi = 300)
