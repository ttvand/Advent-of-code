library(data.table)
data_subfolder <- "2019"
source(file.path(getwd(), data_subfolder, "queue.R"))

data <- fread(file.path(getwd(), data_subfolder, "input06.txt"), header=FALSE)
vals <- data[[1]]
center_object <- "COM"

relations <- unlist(strsplit(vals, ")", fixed=TRUE))
orbits <- t(matrix(relations, nrow=2))
objects <- sort(unique(relations))
num_objects <- length(objects)
paths <- rep("", num_objects)
paths[which(objects == center_object)] <- center_object

obj_q <- new.queue()
enqueue(obj_q, c(center_object, 0))
total_count <- 0
while (!is.empty(obj_q)) {
  head_q <- dequeue(obj_q)
  source_object <- head_q[1]
  direct_relations <- which(orbits[, 1] == source_object)
  for (relation_id in direct_relations){
    prec_length <- as.integer(head_q[2])
    orbiting_object <- orbits[relation_id, 2]
    enqueue(obj_q, c(orbiting_object, prec_length + 1))
    total_count <- total_count + 1 + prec_length
    
    # Update the path
    source_id <- which(source_object == objects)
    orbit_id <- which(orbiting_object == objects)
    paths[orbit_id] <- paste0(paths[source_id], "-", orbiting_object)
  }
}

cat("Part 1:", total_count, "\n")

my_path <- unlist(strsplit(paths[which(objects == "YOU")], "-"))
santa_path <- unlist(strsplit(paths[which(objects == "SAN")], "-"))
common_path <- intersect(my_path, santa_path)
cat("Part 2:", length(my_path) + length(santa_path) - 2*length(common_path) - 2,