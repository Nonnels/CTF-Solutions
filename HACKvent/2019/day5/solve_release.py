from PIL import Image
import binascii

# constants
R,G,B = (0,1,2)
INT_B = []
DEBUG = True

def int_to_ascii(int_array):
    strout = ""
    for i in int_array:
        if i <128 and i > 32:
            try:
                strout+=chr(i)
            except:
                strout+=""
    print(f"ascii: \t{strout}")

def main():
    global R,G,B,INT_B,DEBUG
    # load image and convert to pux
    im = Image.open('157de28f-2190-4c6d-a1dc-02ce9e385b5c.png')
    pix = im.load()
    mX, mY = im.size
    for i in range(mX):
        if DEBUG:
            print (pix[i,0])
        INT_B.append(pix[i,0][B])
        
    print("ASCII:")
    int_to_ascii(INT_B)

if __name__ == "__main__":
	main()
