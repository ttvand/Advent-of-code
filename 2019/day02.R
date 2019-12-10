library(data.table)
data_subfolder <- "2019"

data <- fread(file.path(getwd(), data_subfolder, "input02.txt"))
vals <- as.matrix(data)[1, ]

intcode <- function(vals){
  read_pos <- 1
  while(TRUE){
    read_val <- vals[read_pos]
    if(read_val == 99){
      return (vals)
    } else{
      next1 <- vals[vals[read_pos + 1] + 1]
      next2 <- vals[vals[read_pos + 2] + 1]
      vals[1+vals[read_pos+3]] <- ifelse(read_val==1, next1+next2, next1*next2)
    }
    read_pos <- read_pos + 4
  }
}

# cat(intcode(c(2, 3, 0, 3, 99)), "\n")
# cat(intcode(c(1, 0, 0, 0, 99)), "\n")
# cat(intcode(c(1, 1, 1, 4, 99, 5, 6, 0, 99)), "\n")
part1_vals <- vals; part1_vals[2] <- 12; part1_vals[3] <- 2
cat("Part 1 answer:", intcode(part1_vals)[1], "\n")

# Brute force part 2
found <- FALSE
for(noun in 0:99){
  cat("Noun:", noun, "\n")
  for(verb in 0:99){
    check_vals <- vals
    check_vals[2] <- noun
    check_vals[3] <- verb
    if(intcode(check_vals)[1] == 19690720){
      found <- TRUE
      break
    }
  }
  if(found){
    break
  }
}
cat("Part 2 answer:", 100*noun+verb)