# library(combinat)
library(data.table)
data_subfolder <- "2019"

data <- fread(file.path(getwd(), data_subfolder, "input10.txt"), header=FALSE)
vals <- as.matrix(data)[, 1]
digits <- t(sapply(vals, function(x) substring(x, seq(1, nchar(x), 1),
                                               seq(1, nchar(x), 1))))
nrows <- nrow(digits)
ncols <- ncol(digits)
rownames(digits) <- 1:ncol(digits)

# Find the asteroid positions
num_asteroids <- sum(digits=="#")
positions <- matrix(nrow = num_asteroids, ncol=3)
pos_id <- 1
for(i in 1:nrows){
  for(j in 1:ncols){
    if(digits[i, j] == "#"){
      positions[pos_id, 1:2] <- c(i, j)
      pos_id <- pos_id + 1
    }
  }
}

gcd <- function(x,y) {
  r <- x%%y
  return(ifelse(r, gcd(y, r), y))
}

manhattan_dist <- function(rating1, rating2){
  distance <- abs(rating1-rating2)
  distance <- sum(distance)
  return(distance)
}

get_angle <- function(a, b){
  return(acos( sum(a*b) / ( sqrt(sum(a * a)) * sqrt(sum(b * b)) ) ))
}

angle <- function(M,N){
  acos( sum(M*N) / ( sqrt(sum(M*M)) * sqrt(sum(N*N)) ) )
}
angle2 <- function(M,N){
  atan2(N[2],N[1]) - atan2(M[2],M[1]) 
}

rotation <- function(vec, angle){
  return(c(vec[1]*cos(angle)-vec[2]*sin(angle),
           vec[1]*sin(angle)+vec[2]*cos(angle)))
}

# normalize_direction <- function(distance_vec){
#   if(distance_vec[1] == 0){
#     return(c(0, sign(distance_vec[2])))
#   } else if(distance_vec[2] == 0){
#     return(c( sign(distance_vec[1]), 0))
#   } else{
#     
#     rescaler <- gcd(abs(distance_vec[1]), abs(distance_vec[2]))
#     if(rescaler > 1){
#       distance_vec <- distance_vec/rescaler
#     }
#     return(distance_vec)
#   }
# }
# 
# all_offsets <- t(matrix(rep(-num_asteroids:0, each=2), nrow=2))
# for(i in 1:num_asteroids){
#   seen_asteroids <- rep(TRUE, num_asteroids)
#   seen_asteroids[i] <- FALSE
#   for(j in 1:num_asteroids){
#     if(i != j){
#       orig_distance_vec <- positions[i, 1:2] - positions[j, 1:2]
#       distance_vec <- normalize_direction(orig_distance_vec)
#       considered_offsets <- all_offsets
#       considered_offsets[, 1] <- considered_offsets[, 1]*distance_vec[1]
#       considered_offsets[, 2] <- considered_offsets[, 2]*distance_vec[2]
#       considered_positions <- considered_offsets
#       considered_positions[, 1] <- considered_positions[, 1] + positions[i, 1]
#       considered_positions[, 2] <- considered_positions[, 2] + positions[i, 2]
#       valid_pos <- which(considered_positions[, 1] > 0 & 
#                            considered_positions[, 1] <= ncols &
#                            considered_positions[, 2] > 0 & 
#                            considered_positions[, 2] <= nrows
#       )
#       compare_positions <- considered_positions[valid_pos,]
#       for(k in 1:nrow(compare_positions)){
#         if(manhattan_dist(positions[i, 1:2], compare_positions[k, ]) > sum(
#           abs(orig_distance_vec))){
#           asteroid_match_id <- which(
#             positions[, 1] == compare_positions[k, 1] &
#               positions[, 2] == compare_positions[k, 2])
#           if(length(asteroid_match_id)){
#             seen_asteroids[asteroid_match_id] <- FALSE
#           }
#         }
#       }
#     }
#   }
#   if(positions[i, 1] == 5 && positions[i, 2] == 8) browser()
#   positions[i, 3] <- sum(seen_asteroids)
# }

# cat("Part 1:" max(positions[, 3]))

station_pos <- c(21, 24)
# station_pos <- c(14, 12)
lasered_id <- NULL
laser_dir <- c(-1, 0)
for(i in 1:200){
  if(!is.null(lasered_id)){
    # browser()
    cat(i, nrow(positions), "\n")
    positions <- positions[-lasered_id, ]
  }
  station_pos_id <- which(positions[, 1] == station_pos[1] &
                            positions[, 2] == station_pos[2])
  angles <- apply(positions, 1, function(x) -angle2(
    laser_dir, x[1:2]-positions[station_pos_id, 1:2]))
  angles[station_pos_id] <- NA
  angles[angles<0 & !is.na(angles)] <- angles[angles<0 & !is.na(angles)]+2*pi
  closest_angles <- which(angles == min(angles, na.rm=TRUE))
  distances <- sapply(closest_angles, function(x) sum(
    abs(positions[station_pos_id, 1:2] - positions[x, 1:2])))
  lasered_id <- closest_angles[which.min(distances)]
  
  laser_dir <- positions[lasered_id, 1:2]-positions[station_pos_id, 1:2]
  laser_dir <- rotation(laser_dir, -1e-5)
}

cat(positions[lasered_id, ])