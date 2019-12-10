library(data.table)
data_subfolder <- "2018"

data <- fread(file.path(getwd(), data_subfolder, "input02.txt"), header=FALSE)
vals <- data[[1]]

exact_length_count <- function(x, n){
  chars <- sapply(x, function(x) substring(
    x, seq(1, nchar(x), 1), seq(1, nchar(x), 1)))
  exact_counts <- apply(chars, 2, function(x) n %in% table(x))
  return(sum(exact_counts))
}

find_near_equals <- function(x){
  chars <- sapply(x, function(x) substring(
    x, seq(1, nchar(x), 1), seq(1, nchar(x), 1)))
  num_strings <- ncol(chars)
  for(i in 1:(num_strings-1)){
    for(j in (i+1):num_strings){
      if(sum(chars[, i] != chars[, j]) == 1){
        return(paste0(chars[chars[, i] == chars[, j], i], collapse=""))
      }
    }
  }
  exact_counts <- apply(chars, 2, function(x) n %in% table(x))
  return(sum(exact_counts))
}

pair_count <- exact_length_count(vals, 2)
triple_count <- exact_length_count(vals, 3)
cat("Part 1:", pair_count*triple_count, "\n")
cat("Part 2:", find_near_equals(vals), "\n")