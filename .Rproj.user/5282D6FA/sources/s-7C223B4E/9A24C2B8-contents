library(combinat)
library(data.table)
data_subfolder <- "2019"

data <- fread(file.path(getwd(), data_subfolder, "input08.txt"), header=FALSE)
vals <- unname(as.matrix(data)[1, 1])

nrow <- 25
ncol <- 6
digits <- substring(vals, seq(1, nchar(vals), 1), seq(1, nchar(vals), 1))

digit_counts <- function(vals, digit){
  return(apply(vals, 2, function(x) sum(x==as.character(digit))))
}

channels <- matrix(digits, nrow=nrow*ncol)
zero_counts <- digit_counts(channels, 0)
one_counts <- digit_counts(channels, 1)
two_counts <- digit_counts(channels, 2)
min_zeros_id <- which.min(zero_counts)
cat("Part 1:", one_counts[min_zeros_id]*two_counts[min_zeros_id], "\n")

num_image_pixels <- nrow(channels_transposed)
decoded <- rep(-1, num_image_pixels)
for(i in 1:num_image_pixels){
  first_black <- which(channels[i, ] == 0)
  first_white <- which(channels[i, ] == 1)
  if(length(first_black) > 0){
    if(length(first_white) > 0){
      decoded[i] <- ifelse(first_black[1] < first_white[1], 0, 1)
    } else{
      decoded[i] <- 0
    }
  } else{
    if(length(first_white) > 0){
      decoded[i] <- 1
    } else{
      stop("This should not happen")
    }
  }
}
decoded_img <- matrix(decoded, nrow=nrow, byrow=FALSE)
rotated_decoded_img <- t(apply(decoded_img, 1, rev))
image(rotated_decoded_img)