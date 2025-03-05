#literacy and education are postive, poverty is negative
data <- read.csv("./PS2/Q3/transfer.csv")
#View(data)

cutoff1 <- 10188
cutoff2 <- 13584
cutoff3 <- 16980

population <- data$pop82
data$normalized_pscore <- NA
count <- 0

for (value in population) {
    diff1 <- abs(value - cutoff1)
    diff2 <- abs(value - cutoff2)
    diff3 <- abs(value - cutoff3)

    diff <- pmax(diff1, diff2, diff3)

    if (diff == diff1) {
        diff <- diff / cutoff1 * 100
    }
    else if (diff == diff2) {
        diff <- diff / cutoff2 * 100
    }
    else if (diff == diff3) {
        diff <- diff / cutoff3 * 100
    }

    data$normalized_pscore[count] <- diff
    count <- count + 1

}

View(data)


