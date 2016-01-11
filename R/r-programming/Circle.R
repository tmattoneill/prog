Circle <- function(radius) {
  list (
    area = function() {
      cat ("The area of the circle is", 2 * pi * radius)
    }
  )

}