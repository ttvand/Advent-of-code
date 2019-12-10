library(data.table)
data_subfolder <- "2019"

vals <- 240920:789857
num_digits <- ceiling(log10(tail(vals, 1)))
num_vals <- length(vals)
valid_numbers <- rep(TRUE, num_vals)
adjacent_count <- rep(0, num_vals)
streak_counts <- matrix(0, nrow=num_vals, ncol=num_digits)

for(i in 1:num_digits){
  prev_digit <- vals %% 10
  if(i > 1){
    valid_numbers <- valid_numbers & (prev_digit <= next_digit)
    equal_digits <- prev_digit == next_digit
    adjacent_count <- adjacent_count + equal_digits
    streak_count <- ifelse(equal_digits, prev_streak_count+1, 1)
    equal_ids <- which(equal_digits)
    one_streak_ids <- which(!equal_digits)
    streak_counts[one_streak_ids, 1] <- streak_counts[one_streak_ids, 1] + 1
    for(j in 2:i){
      update_rows <- which(equal_digits & prev_streak_count == (j-1))
      streak_counts[update_rows, j-1] <- streak_counts[update_rows, j-1] - 1
      streak_counts[update_rows, j] <- streak_counts[update_rows, j] + 1
    }
    prev_streak_count <- streak_count
  } else{
    prev_streak_count <- rep(1, num_vals)
    streak_counts[, 1] <- 1
  }
  
  next_digit <- prev_digit
  vals <- vals %/% 10
}
valid_numbers1 <- valid_numbers & (streak_counts[, 1] < num_digits)
valid_numbers2 <- valid_numbers & (streak_counts[, 2] >= 1)
cat(table(valid_numbers1), "\n")
cat(table(valid_numbers2), "\n")
