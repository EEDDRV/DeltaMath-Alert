import math, os, sys

"""
This javascript snippet is from the DeltaMath's website to create a "prelogin factor".
Convert this javascript code to python code:
const processPreloginFactor = (num) => {
  let upper = Math.sqrt(num);
  for (var i = 2; i < upper; i++) {
    if (num % i === 0) {
      return i;
    }
  }
  return num;
};
"""

def processPreloginFactor(num):
	upper = math.sqrt(num)
	for i in range(2, int(upper)):
		if num % i == 0:
			return i
	return num

# If this program is run directly, then use the command line arguments to get the prelogin factor.
if __name__ == "__main__":
	if len(sys.argv) > 1:
		print(processPreloginFactor(int(sys.argv[1])))
	else:
		print("Please provide a prelogin factor.")