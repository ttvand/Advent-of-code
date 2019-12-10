library(data.table)
data_subfolder <- "2018"

data <- fread(file.path(getwd(), data_subfolder, "input01.txt"))
vals <- data[[1]]
cat(sum(vals))

cumsum_vals <- cumsum(c(0, vals))
cumsum_range <- range(cumsum_vals)
match_cumsum <- rep(FALSE, cumsum_range[2] - cumsum_range[1] + 1)
match_cumsum[-cumsum_range[1] + 1] <- TRUE
increment_id <- 1
cumsum <- 0
while(TRUE){
  cat(cumsum, "\n")
  cumsum <- cumsum + vals[increment_id]
  if(cumsum <= cumsum_range[2]){
    if(match_cumsum[-cumsum_range[1] + 1 + cumsum]) break
    match_cumsum[-cumsum_range[1] + 1 + cumsum] <- TRUE
  }
  increment_id <- 1 + (increment_id %% length(vals))
}