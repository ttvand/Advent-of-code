library(combinat)
library(data.table)
library(gmp)
data_subfolder <- "2019"

data <- fread(file.path(getwd(), data_subfolder, "input09.txt"), header=FALSE)
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

intcode <- function(vals, input_value, instr_point=1, input_id=1, rel_base=0){
  memory=matrix(c(as.bigz(NA), as.bigz(NA)), ncol=2)
  vals <- as.bigz(vals)
  while(TRUE){
    if(sum(is.na(vals)) > 0){
      browser()
    }
    # cat(instr_point, "\n")
    read_val <- vals[as.integer(instr_point)]
    opcode <- read_val %% 100
    # cat(vals, "\n")
    cat(as.integer(instr_point), as.integer(opcode), as.integer(rel_base),
        as.integer(read_val), "\n")
    # cat(as.integer(vals[instr_point:(instr_point+4)]), "\n")
    if(opcode == 99){
      browser()
      return (list(output_val=NA, vals=vals, instr_point=instr_point,
                   halted=TRUE))
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
      # if(output_val != 0){
      if(instr_point > 904){
        browser()
        return(list(output_val=output_val, vals=vals, instr_point=instr_point,
                    halted=FALSE))
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
        third <- read_mem_val(
          vals, as.integer(vals[as.integer(instr_point + 3)] + rel_base),
          memory)
      } else{
        third <- vals[as.integer(instr_point + 3)]
      }
      condition <- as.integer((opcode == 7 && first < second) || (
        opcode == 8 && first == second))
      write_vals <- write(vals, condition, third, read_val, 4, rel_base, memory,
                          overwrite_imm_mode=TRUE)
      vals <- write_vals$vals
      if(instr_point==500){
        browser()
        vals[500] <- 0
      }
      if(instr_point==816){
        browser()
        vals[816] <- 0
      }
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

# cat(intcode(c(109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99), NA)$vals)
# cat(intcode(c(1102,34915192,34915192,7,4,7,99,0), NA)$output_val)
cat("Part 1:", intcode(vals, 1)$output_val)

# perms <- permn(1:5)
# num_perms <- length(perms)
# max_signal_1 <- 0
# # for(i in 1:num_perms){
# #   cat(i, ":")
# #   input2 <- 0
# #   for(step in 1:5){
# #     input1 <- perms[[i]][step]-1
# #     output <- intcode(vals, c(input1, input2))
# #     input2 <- output 
# #   }
# #   cat(output, "\n")
# #   if(output > max_signal_1){
# #     max_signal_1 <- output
# #   }
# # }
# 
# # vals <- c(3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26, 27,4,27,1001,28,-1,28,
# #           1005,28,6,99,0,0,5)
# max_signal_2 <- 0
# for(i in 1:num_perms){
#   cat(i, ":")
#   input2 <- 0
#   halted <- FALSE
#   all_states <- rep(list(list(vals=vals, instr_point=1)), 5)
#   first_loop <- TRUE
#   while(!halted){
#     for(step in 1:5){
#       if(i == 17){
#         browser()
#       }
#       step_inputs <- input2
#       if(first_loop){
#          step_inputs <- c(perms[[i]][step]+4, step_inputs)
#       }
#       all_outputs <- intcode(all_states[[step]]$vals, step_inputs,
#                              all_states[[step]]$instr_point)
#       all_states[[step]] <- all_outputs
#       prev_output <- all_outputs$output_val
#       input2 <- prev_output
#     }
#     first_loop <- FALSE
#     halted <- all_outputs$halted
#     if(!halted){
#       last_output <- all_outputs$output
#     }
#   }
#   cat(last_output, "\n")
#   if(last_output > max_signal_2){
#     max_signal_2 <- last_output
#   }
# }
# 
# cat("Part 1:", max_signal_1, "\n")
# cat("Part 2:", max_signal_2, "\n")