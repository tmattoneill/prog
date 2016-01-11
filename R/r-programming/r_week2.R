add2 <- function(x, y){
  x+y
}

above <- function(v, n=10){
  # v is a vector passed in
  use <- x > n
  x[use]
}

column_mean <- function(y, remove_na=TRUE){
  nc <- ncol(y)
  means <- numeric(nc)
  for(i in 1:nc) {
    means[i] <- mean(y[,i], na.rm = removeNA)
  }
  means
}