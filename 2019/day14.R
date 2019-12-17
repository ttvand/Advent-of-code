## Get the input
reactions <- readLines(file.path(getwd(), "2019", "input14.txt"))

# Distill the reactions into inputs and outputs
reaction_parts <- strsplit(reactions, "=>")
num_reactions <- length(reaction_parts)
inputs <- vector(mode="list", length=num_reactions)
outputs <- matrix(nrow=num_reactions, ncol=2)
trim <- function (x) gsub("^\\s+|\\s+$", "", x)
for(i in 1:num_reactions){
  reaction_inputs <- strsplit(reaction_parts[[i]][1], ",")[[1]]
  num_reaction_inputs <- length(reaction_inputs)
  inputs[[i]] <- matrix(nrow=num_reaction_inputs, ncol=2)
  for(j in 1:num_reaction_inputs){
    inputs[[i]][j, ] <- strsplit(trim(reaction_inputs[j]), " ")[[1]]
  }
  outputs[i, ] <- strsplit(trim(reaction_parts[[i]][2]), " ")[[1]]
}

# List all elements
unique_elements <- unique(
  unlist(c(outputs[, 2], sapply(inputs, function(x) x[, 2]))))
num_unique_elements <- length(unique_elements)
element_costs <- matrix(nrow=num_unique_elements, ncol=6)
colnames(element_costs) <- c("Element", "Cost", "All considered",
                             "Num_reactions", "Base count", "Target count")
element_costs[, 1] <- unique_elements
element_costs[, 3] <- FALSE
element_costs[, 4] <- sapply(unique_elements, function(x) sum(
  outputs[, 2] == x))
element_costs[which(unique_elements == "ORE"), 2] <- 1
element_costs[which(unique_elements == "ORE"), 3] <- TRUE
while(TRUE){
  # List the reactions we can make with the available elements
  completed_elements <- which(as.logical(element_costs[, 3]))
  input_elements <- element_costs[completed_elements, 1]
  possible_reaction_ids <- which(unlist(lapply(
    inputs, function(x) all(x[, 2] %in% input_elements))))
  valid_reactions <- setdiff(possible_reaction_ids, completed_elements)
  for(i in valid_reactions){
    browser()
  }
}