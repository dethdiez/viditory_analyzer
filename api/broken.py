from subprocess import call
import json

def CheckBroken(name):
	with open("errResponse.txt", "w") as errResponse:
		call (["ffmpeg", "-v", "error", "-i", name, "-f", "null"], stderr = errResponse)

	flag = True
	with open("errResponse.txt", "r") as f:
		data = f.read(42)
		flag = True
		if data == "At least one output file must be specified":
			flag = False
	return flag

def main():
	pass
#	print(CheckBroken("11422.avi"))
#	print(CheckBroken("example.mp4"))

if __name__ == '__main__':
    main()