new.queue <- function() {
  ret <- new.env()
  ret$front <- new.env()
  ret$front$q <- NULL
  ret$front$prev <- NULL
  ret$last <- ret$front
  return(ret)
}

## add to end of queue
enqueue <- function(queue, add){
  queue$last$q <- new.env()
  queue$last$q$prev <- queue$last
  queue$last <- queue$last$q
  queue$last$val <- add
  queue$last$q <- NULL
}

## return front of queue and remove it
dequeue <- function(queue){
  if (is.empty(queue)) {
    stop("Attempting to take element from empty queue")
  }
  value <- queue$front$q$val
  queue$front <- queue$front$q
  queue$front$q$prev <- NULL
  return(value)
}

is.empty <- function(queue){
  return(is.null(queue$front$q))
}