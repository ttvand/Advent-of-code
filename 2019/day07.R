library(combinat)
library(data.table)
data_subfolder <- "2019"

data <- fread(file.path(getwd(), data_subfolder, "input07.txt"), header=FALSE)
vals <- unname(as.matrix(data)[1, ])

read_pos_or_param <- function(vals, argument, mode, pos_mode){
  if(mode %/% 10^(pos_mode) %% 10 == 0){
    # Position mode
    return(vals[vals[argument] + 1])
  } else{
    # Immediate mode
    return(vals[argument])
  }
}

write_pos_or_param <- function(vals, write_val, write_pos, mode, pos_mode,
                               overwrite_imm_mode=FALSE){
  if(mode %/% 10^(pos_mode) %% 10 == 0 && !overwrite_imm_mode){
    # Position mode
    vals[1+vals[write_pos]] <- write_val
  } else{
    # Immediate mode
    vals[1+write_pos] <- write_val
  }
  return(vals)
}

intcode <- function(vals, input_value, instr_point=1, input_id=1){
  # browser()
  while(TRUE){
    if(sum(is.na(vals)) > 0){
      browser()
    }
    # cat(instr_point, "\n")
    read_val <- vals[instr_point]
    opcode <- read_val %% 100
    # cat(vals, "\n")
    if(opcode == 99){
      return (list(output_val=NA, vals=vals, instr_point=instr_point,
                   halted=TRUE))
    } else if(opcode == 1 || opcode == 2){
      next1 <- read_pos_or_param(vals, instr_point + 1, read_val, 2)
      next2 <- read_pos_or_param(vals, instr_point + 2, read_val, 3)
      vals <- write_pos_or_param(vals, ifelse(
        opcode==1, next1+next2, next1*next2), instr_point + 3, read_val, 4)
      instr_point <- instr_point + 4
    } else if(opcode == 3){
      vals <- write_pos_or_param(vals, input_value[input_id], instr_point + 1,
                                 read_val, 2)
      input_id <- min(length(input_value), input_id + 1)
      instr_point <- instr_point + 2
    }
    else if(opcode == 4){
      # browser()
      output_val <- read_pos_or_param(vals, instr_point + 1, read_val, 2)
      instr_point <- instr_point + 2
      if(is.na(output_val)){
        output_val = NA
      }
      if(output_val != 0){
        return(list(output_val=output_val, vals=vals, instr_point=instr_point,
                    halted=FALSE))
      }
    } else if(opcode == 5 || opcode == 6){
      condition <- read_pos_or_param(vals, instr_point + 1, read_val, 2)
      if(xor(opcode == 5, condition == 0)){
        instr_point <- read_pos_or_param(vals, instr_point + 2, read_val, 3)+1
      } else{
        instr_point <- instr_point + 3
      }
    } else if(opcode == 7 || opcode == 8){
      first <- read_pos_or_param(vals, instr_point + 1, read_val, 2)
      second <- read_pos_or_param(vals, instr_point + 2, read_val, 3)
      third <- vals[instr_point + 3]
      condition <- as.integer((opcode == 7 && first < second) || (
        opcode == 8 && first == second))
      vals <- write_pos_or_param(vals, condition, third, read_val, 4,
                                 overwrite_imm_mode=TRUE)
      instr_point <- instr_point + 4
    } else{
      errorCondition("Unsupported opcode")
    }
  }
}

perms <- permn(1:5)
num_perms <- length(perms)
max_signal_1 <- 0
# for(i in 1:num_perms){
#   cat(i, ":")
#   input2 <- 0
#   for(step in 1:5){
#     input1 <- perms[[i]][step]-1
#     output <- intcode(vals, c(input1, input2))
#     input2 <- output 
#   }
#   cat(output, "\n")
#   if(output > max_signal_1){
#     max_signal_1 <- output
#   }
# }

# vals <- c(3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26, 27,4,27,1001,28,-1,28,
#           1005,28,6,99,0,0,5)
max_signal_2 <- 0
for(i in 1:num_perms){
  cat(i, ":")
  input2 <- 0
  halted <- FALSE
  all_states <- rep(list(list(vals=vals, instr_point=1)), 5)
  first_loop <- TRUE
  while(!halted){
    for(step in 1:5){
      if(i == 17){
        browser()
      }
      step_inputs <- input2
      if(first_loop){
         step_inputs <- c(perms[[i]][step]+4, step_inputs)
      }
      all_outputs <- intcode(all_states[[step]]$vals, step_inputs,
                             all_states[[step]]$instr_point)
      all_states[[step]] <- all_outputs
      prev_output <- all_outputs$output_val
      input2 <- prev_output
    }
    first_loop <- FALSE
    halted <- all_outputs$halted
    if(!halted){
      last_output <- all_outputs$output
    }
  }
  cat(last_output, "\n")
  if(last_output > max_signal_2){
    max_signal_2 <- last_output
  }
}

cat("Part 1:", max_signal_1, "\n")
cat("Part 2:", max_signal_2, "\n")