# my shitty attempt at creating an ASCII art generator :-PPP

### TODO

* Dealing with spaghetti when changing to ascii
* Moving the text into image (finding the right size etc) if image scaling will be implemented
* Coloring the letters if text is moved
* Trying to show the art in terminal if that will work
* Making the function to auto-generate ASCII letters in different styles
* Making a website out of this
* Dockerise it?

### DONE
* Image scaling for both x and y coords
  + the code is fucking spaghetti and slow (it was alright for some time but rn it has ~0.3 seconds longer compute time)
  + it has to be only one loop instead of two, it creates complexity, we should have circa 0.04 compute time but we have 0.04^3 (while loop takes a lot of time)
  + possible solution is to only iterate through x and make x / scale_X arrays of pixels, and clear it on the scale_x time
  + da sie to zrobic jednym for loopem liczac ile bedzie razem przejść w obrazie na gridzie + jedno modulo i zwiekszajac x patrzac na y 
  + numpy?
  + search function is completely unnecessary, but 