import sys

'''
   This file is meant to be called at the command line.
   Assume we are dealing with large databases. Use BASH to stream
   input. 
'''

if __name__ == "__main__":
	for line in sys.stdin:
		sys.stderr.write(line)