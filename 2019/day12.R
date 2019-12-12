library(combinat)
library(data.table)
library(gmp)
data_subfolder <- "2019"

steps <- 1000

data <- fread(file.path(getwd(), data_subfolder, "input12.txt"), header=FALSE)
vals <- as.matrix(data)
initial_positions <- apply(
  vals, 2, function(x) as.numeric(gsub(".*=|>", "", x)))
positions <- initial_positions
num_objects <- nrow(positions)
num_dim <- ncol(positions)
velocities <- matrix(0, nrow=num_objects, ncol=num_dim)

for(i in 1:steps){
  # Gravity
  for(j in 1:num_dim){
    dim_vals <- positions[, j]
    count_incr <- sapply(dim_vals, function(x) sum(x < dim_vals))
    count_decr <- sapply(dim_vals, function(x) sum(x > dim_vals))
    velocities[, j] <- velocities[, j] + count_incr - count_decr
  }
  
  # Velocity
  positions <- positions + velocities
}

cat("Part 1:", sum(rowSums(abs(positions))*rowSums(abs(velocities))))

# Part 2: consider x, y and z cycles and compute lcm
cycle_length <- function(positions, max_cycle_length=1000000){
  num_objects <- length(positions)
  prev_positions <- matrix(NA, nrow=max_cycle_length, ncol=num_objects)
  prev_positions[1, ] <- positions
  velocities <- rep(0, num_objects)
  rep_steps <- c()
  for(j in 2:max_cycle_length){
    count_incr <- sapply(positions, function(x) sum(x < positions))
    count_decr <- sapply(positions, function(x) sum(x > positions))
    velocities <- velocities + count_incr - count_decr
    
    positions <- positions + velocities
    
    # Look for initial position matches
    if(sum(abs(positions - prev_positions[1, ])) == 0) return(j)    prev_positions[j, ] <- positions
  }
}
cycle_lengths <- apply(initial_positions, 2, cycle_length)
cat("Part 2:",
    lcm.bigz(lcm.bigz(cycle_lengths[1], cycle_lengths[2]), cycle_lengths[3]))
