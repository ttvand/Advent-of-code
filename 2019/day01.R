library(data.table)
data_subfolder <- "2019"

data <- fread(file.path(getwd(), data_subfolder, "input01.txt"))
vals <- data[[1]]
consumption_sum <- sum(floor(vals/3)-2)
cat("Summed fuel requirement:", consumption_sum)

total_fuel_consumption <- 0
remaining_weight <- vals
while(max(remaining_weight) > 0){
  cat("Remaining weight range:", range(remaining_weight), "\n")
  remaining_weight <- pmax(0, floor(remaining_weight/3)-2)
  total_fuel_consumption <- total_fuel_consumption + sum(remaining_weight)
}
cat("Total fuel consumption:", total_fuel_consumption)