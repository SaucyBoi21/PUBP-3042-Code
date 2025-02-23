data <- read.csv("turnout-1.csv")

print(dim(data))
print(summary(data))

vap_turnout <- ((data$total) / (data$VAP + data$overseas)) * 100
print(paste0("VAP turnout rate for ", data$year, ": ", vap_turnout))

vep_turnout <- ((data$total) / (data$VEP)) * 100
print(paste0("VEP turnout rate for ", data$year, ": ", vep_turnout))

vap_difference <- data$ANES - vap_turnout

mean_vap_difference <- mean(vap_difference)
range_vap_difference <- max(vap_difference) - min(vap_difference)
print(paste0("Mean Difference between VAP & ANES Turnout: ", mean_vap_difference))
print(paste0("Range in Difference between VAP & ANES Turnout: ", range_vap_difference))

vep_difference <- data$ANES - vep_turnout

mean_vep_difference <- mean(vep_difference)
range_vep_difference <- max(vep_difference) - min(vep_difference) 
print(paste0("Mean Difference between VEP & ANES Turnout: ", mean_vep_difference))
print(paste0("Range in Difference between VEP & ANES Turnout: ", range_vep_difference))


pres_years <- data[data$year %% 4 == 0, ]
pres_years$turnout <- (pres_years$total / pres_years$VEP) * 100
pres_years_anes <- pres_years$ANES
pres_years_difference <- pres_years_anes - pres_years$turnout
mean_pres_years_difference <- mean(pres_years_difference)

print(paste0("Mean Difference between ANES and VEP turnout during Presidential Election Years: ", mean_pres_years_difference))

mid_years <- data[data$year %% 4 != 0, ]
mid_years$turnout <- (mid_years$total / mid_years$VEP) * 100
mid_years_anes <- mid_years$ANES
mid_years_difference <- mid_years_anes - mid_years$turnout
mean_mid_years_difference <- mean(mid_years_difference)

print(paste0("Mean Difference between ANES and VEP turnout during Midterm Election Years: ", mean_mid_years_difference))

start_vep_turnout <- (data[1:7, ]$total / data[1:7, ]$VEP) * 100
start_anes <- data[1:7,]$ANES
start_difference <- start_anes - start_vep_turnout
mean_start_diff <- mean(start_difference)

print(paste0("Mean Difference between ANES and VEP turnout from 1980 to 1992: ", mean_start_diff))

end_vep_turnout <- (data[8:14, ]$total / data[8:14, ]$VEP) * 100
end_anes <- data[8:14, ]$ANES
end_difference <- end_anes - end_vep_turnout
mean_end_diff <- mean(end_difference)

print(paste0("Mean Difference between ANES and VEP turnout from 1994 to 2008: ", mean_end_diff))






