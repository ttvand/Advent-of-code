## Since the intcode computer is finished now I'll keep it separate
source(file.path(getwd(), "2019", "run_intcode_step.R"))

## Get the program
program <- as.numeric(strsplit(readLines(
  file.path(getwd(), "2019", "input13.txt")), ",")[[1]])

## Collect output
all_outputs <- rep(NA, 10000)
output_step <- 1
intcode_state <- list(mmry = program)
while(TRUE){
  intcode_state <- run_intcode_step(intcode_state, NA)
  if(intcode_state$halted){
    all_outputs <- all_outputs[1:(output_step-1)]
    break
  }
  step_output <- intcode_state$output
  
  all_outputs[output_step] <- step_output
  output_step <- output_step + 1
}

get_game <- function(outputs){
  outputs_m <- matrix(outputs, nrow=3)
  max_first <- max(outputs_m[1, ]) + 1
  max_sec <- max(outputs_m[2, ]) + 1
  num_entries <- ncol(outputs_m)
  game <- matrix(NA, nrow=max_first, ncol=max_sec)
  for(i in 1:num_entries){
    game[outputs_m[1, i]+1, outputs_m[2, i]+1] <- outputs_m[3, i]
  }
  
  return(game)
}

game <- get_game(all_outputs)
cat("Part 1:", sum(game==2), "\n")

# Play for free in part 2
program2 <- program
program2[1] <- 2
intcode_state <- list(mmry = program2)

# Collect outputs and make sure the ball doesn't bounce off the screen
step_2_outputs <- rep(NA, 100000)
output_step_2 <- 1
ball_pos <- NULL
paddle_pos <- NULL
joystick_default <- 0
while(TRUE){
  if(!is.null(ball_pos) && !is.null(paddle_pos)){
    joystick_action <- (ball_pos[1]>paddle_pos[1])*1 + (
      ball_pos[1]<paddle_pos[1])*(-1)
  } else{
    joystick_action <- joystick_default
  }
  intcode_state <- run_intcode_step(intcode_state, joystick_action)
  if(intcode_state$halted){
    step_2_outputs <- step_2_outputs[1:(output_step_2-1)]
    break
  }
  step_output <- intcode_state$output
  
  step_2_outputs[output_step_2] <- step_output
  output_step_2 <- output_step_2 + 1
  
  if((output_step_2-1) %% 3 == 0){
    if(step_output == 4){
      # Update the ball position
      if(!is.null(ball_pos))
      ball_pos <- c(step_2_outputs[output_step_2-3],
                    step_2_outputs[output_step_2-2])
      cat("Ball pos:", ball_pos, "\n")
    }
    if(step_output == 3){
      # Update the paddle position
      paddle_pos <- c(step_2_outputs[output_step_2-3],
                      step_2_outputs[output_step_2-2])
      cat("Paddle pos:", paddle_pos, "\n")
    }
  }
}

game2 <- get_game(step_2_outputs)
outputs_2_m <- matrix(step_2_outputs, nrow=3)
score_cols <- which(outputs_2_m[1,] == -1)
cat("Part 2:", outputs_2_m[3, max(score_cols)], "\n")
