library(data.table)
data_subfolder <- "2019"

data <- fread(file.path(getwd(), data_subfolder, "input05.txt"))
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

intcode <- function(vals, input_value){
  instr_point <- 1
  while(TRUE){
    # cat(instr_point, "\n")
    read_val <- vals[instr_point]
    opcode <- read_val %% 100
    # cat(vals, "\n")
    if(opcode == 99){
      return (vals)
    } else if(opcode == 1 || opcode == 2){
      next1 <- read_pos_or_param(vals, instr_point + 1, read_val, 2)
      next2 <- read_pos_or_param(vals, instr_point + 2, read_val, 3)
      vals <- write_pos_or_param(vals, ifelse(
        opcode==1, next1+next2, next1*next2), instr_point + 3, read_val, 4)
      instr_point <- instr_point + 4
    } else if(opcode == 3){
      vals <- write_pos_or_param(vals, input_value, instr_point + 1, read_val, 2)
      instr_point <- instr_point + 2
    }
    else if(opcode == 4){
      # browser()
      output_val <- read_pos_or_param(vals, instr_point + 1, read_val, 2)
      if(output_val != 0){
        return(output_val)
      }
      instr_point <- instr_point + 2
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

cat("Part 1:", intcode(vals, 1), "\n")
cat("Part 2:", intcode(vals, 5), "\n")

# cat(intcode(c(3,3,1108,-1,8,3,4,3,99), 7))