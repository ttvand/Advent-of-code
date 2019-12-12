library(combinat)
library(data.table)
library(gmp)
data_subfolder <- "2019"

data <- fread(file.path(getwd(), data_subfolder, "input11.txt"), header=FALSE)
vals <- unname(as.matrix(data)[1, ])
vals <- as.bigz(vals)

read_mem_val <- function(vals, argument, memory){
  if(argument <= length(vals)){
    return(vals[as.integer(argument)])
  } else{
    memory_match_id <- which(memory[, 1] == as.vector(argument))
    if(length(memory_match_id) > 0){
      return(memory[memory_match_id[1], 2])
    } else{
      return (0)
    }
  }
}

write_mem_val <- function(vals, argument, write_value, memory){
  if(argument <= length(vals)){
    vals[as.integer(argument)] <- write_value
  } else{
    memory_match_id <- which(memory[, 1] == as.vector(argument))
    # cat("argument:", as.integer(argument), "\n")
    if(length(memory_match_id) > 0){
      memory[memory_match_id, 2] <- write_value
    } else{
      memory_size <- nrow(memory)
      new_memory <- matrix(as.bigz(NA), nrow=memory_size+1, ncol=2)
      new_memory[1:memory_size,] <- memory
      memory <- new_memory
      memory[memory_size+1,] <- c(argument, write_value)
    }
  }
  return(list("vals"=vals, "memory"=memory))
}

read <- function(vals, argument, mode, pos_mode, rel_base, memory, debug=FALSE){
  operation_mode <- mode %/% 10^(pos_mode) %% 10
  if(debug) browser()
  if(operation_mode == 0){
    # Position mode
    sub_read_pos <- read_mem_val(vals, argument, memory)+1
    return(read_mem_val(vals, sub_read_pos, memory))
    # return(vals[vals[argument] + 1])
  } else if(operation_mode == 1){
    # Immediate mode
    # return(vals[argument])
    return(read_mem_val(vals, argument, memory))
  } else if(operation_mode == 2){
    # Relative mode
    # return(vals[vals[argument+rel_base] + 1])
    return(read_mem_val(vals, read_mem_val(vals, argument, memory)+rel_base+1,
                        memory))
  } else{
    browser()
  }
}

write <- function(vals, write_val, write_pos, mode, pos_mode, rel_base, memory,
                  overwrite_imm_mode=FALSE){
  operation_mode <- mode %/% 10^(pos_mode) %% 10
  # if (overwrite_imm_mode) browser()
  if(operation_mode == 0 && !overwrite_imm_mode){
    # Position mode
    # vals[1+read_mem_val(vals, write_pos, memory)] <- write_val
    write_output <- write_mem_val(vals, 1+read_mem_val(vals, write_pos, memory),
                                  write_val, memory)
  } else if (operation_mode == 1 || overwrite_imm_mode){
    # Immediate mode
    # vals[1+write_pos] <- write_val
    write_output <- write_mem_val(vals, 1+write_pos, write_val, memory)
  } else if (operation_mode == 2){
    # Relative mode
    # vals[1+read_mem_val(vals, write_pos+rel_base, memory)] <- write_val
    write_output <- write_mem_val(vals, 1+rel_base+read_mem_val(
      vals, write_pos, memory), write_val, memory)
  } else{
    browser()
  }
  return(write_output)
}

intcode <- function(vals, input_value, instr_point=1, input_id=1, rel_base=0,
                    memory=NULL, return_zero_vals=TRUE){
  if(is.null(memory)){
    memory=matrix(c(as.bigz(NA), as.bigz(NA)), ncol=2)
  }
  vals <- as.bigz(vals)
  output_val <- NULL
  while(TRUE){
    if(sum(is.na(vals)) > 0){
      browser()
    }
    # cat(instr_point, "\n")
    read_val <- vals[as.integer(instr_point)]
    opcode <- read_val %% 100
    # cat(vals, "\n")
    
    # cat(as.integer(instr_point), as.integer(opcode), "\n")
    # cat(as.integer(vals[instr_point:(instr_point+4)]), "\n")
    if(opcode == 99){
      # browser()
      return (list(output_val=NA, vals=vals, instr_point=instr_point,
                   rel_base=rel_base, memory=memory,
                   halted=TRUE, last_output_val=output_val))
    } else if(opcode == 1 || opcode == 2){
      next1 <- read(vals, instr_point + 1, read_val, 2, rel_base, memory)
      next2 <- read(vals, instr_point + 2, read_val, 3, rel_base, memory)
      write_value <- if(opcode==1) add.bigz(next1, next2) else mul.bigz(next1, next2)
      write_vals <- write(vals, write_value, instr_point + 3, read_val, 4,
                          rel_base, memory)
      vals <- write_vals$vals
      memory <- write_vals$memory
      instr_point <- instr_point + 4
    } else if(opcode == 3){
      write_vals <- write(vals, input_value[input_id], instr_point + 1,
                          read_val, 2, rel_base, memory)
      vals <- write_vals$vals
      memory <- write_vals$memory
      input_id <- min(length(input_value), input_id + 1)
      instr_point <- instr_point + 2
    }
    else if(opcode == 4){
      output_val <- read(vals, instr_point + 1, read_val, 2, rel_base, memory)
      instr_point <- instr_point + 2
      if(is.na(output_val)){
        output_val = NA
      }
      if(output_val > 0 || return_zero_vals){
        return(list(output_val=output_val, vals=vals, instr_point=instr_point,
                    rel_base=rel_base, memory=memory, halted=FALSE))
      }
    } else if(opcode == 5 || opcode == 6){
      condition <- read(vals, instr_point + 1, read_val, 2, rel_base, memory)
      if(xor(opcode == 5, condition == 0)){
        instr_point <- read(vals, instr_point + 2, read_val, 3, rel_base, memory) + 1
      } else{
        instr_point <- instr_point + 3
      }
    } else if(opcode == 7 || opcode == 8){
      first <- read(vals, instr_point + 1, read_val, 2, rel_base, memory)
      second <- read(vals, instr_point + 2, read_val, 3, rel_base, memory)
      # third <- read(vals, instr_point + 3, read_val, 4, rel_base, memory,
      #               debug=(instr_point==5))
      if(read_val %/% 10000 == 2){
        third <- vals[as.integer(instr_point + 3)] + rel_base
      } else if(read_val %/% 10000 == 1){
        third <- vals[as.integer(instr_point + 3)]
      } else{
        third <- as.integer(instr_point + 3)
      }
      condition <- as.integer((opcode == 7 && first < second) || (
        opcode == 8 && first == second))
      write_vals <- write(vals, condition, third, read_val, 4, rel_base, memory,
                          overwrite_imm_mode=TRUE)
      vals <- write_vals$vals
      # if(instr_point==500){
      #   browser()
      # vals[500] <- 0
      # }
      # if(instr_point==816){
      #   browser()
      # vals[816] <- 0
      # }
      memory <- write_vals$memory
      instr_point <- instr_point + 4
    } else if(opcode == 9){
      base_incr <- read(vals, instr_point + 1, read_val, 2, rel_base, memory)
      rel_base <- rel_base + base_incr
      instr_point <- instr_point + 2
    }
    else{
      errorCondition("Unsupported opcode")
    }
  }
}


max_grid_size <- 200
start_pos <- floor(max_grid_size/2)
colors <- matrix(0, nrow=max_grid_size, ncol=max_grid_size)
visited <- matrix(FALSE, nrow=max_grid_size, ncol=max_grid_size)
halted <- FALSE
# UP, RIGHT, DOWN, LEFT
direction <- c(-1, 0)
directions <- matrix(c(-1, 0, 0, 1, 1, 0, 0, -1), byrow=TRUE, ncol=2)
pos <- c(start_pos, start_pos)
step_outputs <- NULL
override_first_inputs <- TRUE # Set to TRUE for PART 2
if(override_first_inputs){
  colors[pos[1], pos[2]] <- 1
  direction <- c(-1, 0)
}
while(!halted){
  step_inputs <- colors[pos[1], pos[2]]
  if(is.null(step_outputs)){
    step_outputs <- intcode(
      vals=vals,
      input_value=rep(step_inputs, 100),
      instr_point=1,
      rel_base=0,
      memory=NULL
      )
  } else{
    if(pos[1] == start_pos && pos[2] == start_pos) browser()
    step_outputs <- intcode(
      vals=step_outputs$vals,
      input_value=rep(step_inputs, 100),
      instr_point=step_outputs$instr_point,
      rel_base=step_outputs$rel_base,
      memory=step_outputs$memory
    )
  }
  paint_color <- as.integer(step_outputs$output_val)
  
  # browser()
  
  step_outputs <- intcode(
    vals=step_outputs$vals,
    input_value=rep(step_inputs, 100),
    instr_point=step_outputs$instr_point,
    rel_base=step_outputs$rel_base,
    memory=step_outputs$memory
  )
  dir_change_output <- as.integer(step_outputs$output_val)
  halted <- step_outputs$halted
  
  # Process the program outputs
  visited[pos[1], pos[2]] <- TRUE
  colors[pos[1], pos[2]] <- paint_color
  dir_id <- which(directions[, 1] == direction[1] &
                    directions[, 2] == direction[2])
  if(dir_change_output == 0){
    # Turn left
    dir_id <- 1+((dir_id - 2) %% 4)
  } else if(dir_change_output==1){
    # Turn right
    dir_id <- 1+(dir_id %% 4)
  } else{
    browser()
    stop("This should not happen")
  }
  direction <- directions[dir_id,]
  pos[1] <- pos[1] + direction[1]
  pos[2] <- pos[2] + direction[2]
  cat(pos, paint_color, "\n")
}

rotated_img <- t(apply(colors, 1, rev))
rotated_img <- t(apply(matrix(as.numeric(visited), nrow=max_grid_size), 1, rev))
image(rotated_img)
