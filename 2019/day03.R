library(data.table)
data_subfolder <- "2019"

data <- fread(file.path(getwd(), data_subfolder, "input03.txt"), header=FALSE)
data <- as.matrix(data)

line_segments <- function(path){
  num_steps <- length(path)
  segments <- matrix(0, nrow=num_steps, ncol=5)
  directions <- substr(path, 1, 1)
  values <- as.numeric(substring(path, 2))
  segments[2:num_steps, 5] <- cumsum(values[1:(num_steps-1)])
  value_sign <- ifelse(directions %in% c("L", "D"), -values, values)
  position <- c(0, 0)
  for(i in 1:num_steps){
    if(i %% 2 == 1){
      next_position <- c(position[1] + value_sign[i], position[2])
    } else{
      next_position <- c(position[1], position[2] + value_sign[i])
    }
    segments[i, 1:4] <- c(position, next_position)
    position <- next_position
  }
  return(segments)
}

closest_intersection <- function(segments1, segments2){
  closest_distance <- Inf
  min_path_length_sum <- Inf
  xmax1 <- pmax(segments1[, 1], segments1[, 3])
  xmin1 <- pmin(segments1[, 1], segments1[, 3])
  xmax2 <- pmax(segments2[, 1], segments2[, 3])
  xmin2 <- pmin(segments2[, 1], segments2[, 3])
  ymax1 <- pmax(segments1[, 2], segments1[, 4])
  ymin1 <- pmin(segments1[, 2], segments1[, 4])
  ymax2 <- pmax(segments2[, 2], segments2[, 4])
  ymin2 <- pmin(segments2[, 2], segments2[, 4])
  for(i in 1:nrow(segments1)){
    consider <- which(xmax1[i] >= xmin2 & xmax2 >= xmin1[i] &
                        ymax1[i] >= ymin2 & ymax2 >= ymin1[i])
    for(j in consider){
      if(i %% 2 == 1 && j %% 2 ==1){
        # Both horizontal
        xintersect <- intersect(xmin1[i]:xmax1[i], xmin2[j]:xmax2[j])
        intersect_min_manh_diff <- min(abs(xintersect)) + abs(ymin1[i])
        path_length_sum <- segments1[i, 5] + segments2[j, 5] + abs(
          segments1[i, 1] - segments2[j, 1])
      }
      else if(i %% 2 == 0 && j %% 2 == 0){
        # Both vertical
        yintersect <- intersect(ymin1[i]:ymax1[i], ymin2[j]:ymax2[j])
        intersect_min_manh_diff <- min(abs(yintersect)) + abs(xmin1[i])
        path_length_sum <- segments1[i, 5] + segments2[j, 5] + abs(
          segments1[i, 2] - segments2[j, 2])
      } else{
        # Intersecting
        intersect_min_manh_diff <- ifelse(
          i %% 2 == 0, abs(segments1[i, 1]) + abs(segments2[j, 2]),
          abs(segments1[i, 2]) + abs(segments2[j, 1]))
        path_length_sum <- segments1[i, 5] + segments2[j, 5] + sum(abs(
          segments1[i, 1:2] - segments2[j, 1:2]))
      }
      if(intersect_min_manh_diff > 0){
        if(intersect_min_manh_diff < closest_distance){
          closest_distance <- intersect_min_manh_diff
        }
        if(path_length_sum < min_path_length_sum){
          min_path_length_sum <- path_length_sum
        }
      }
    }
  }
  return(c(closest_distance, min_path_length_sum))
}
segments1 <- line_segments(data[1, ])
segments2 <- line_segments(data[2, ])
intersect_results <- closest_intersection(segments1, segments2)
cat("Closest intersection:", intersect_results[1], "\n")
cat("Minimum path length:", intersect_results[2], "\n")