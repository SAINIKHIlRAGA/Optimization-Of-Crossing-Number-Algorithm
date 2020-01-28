from PIL import Image

img1 = Image.open('LAND2(1).BMP', 'r').convert('RGB')
width1 = img1.size[0]
height1 = img1.size[1]
pix1 = list()
for y in range(0, height1): #each pixel has coordinates
    row = ""
    for x in range(0, width1):

        RGB = img1.getpixel((x, y))
        pix1.append(RGB)

img2 = Image.open('output1(1).bmp', 'r').convert('RGB')
width2 = img1.size[0]
height2 = img1.size[1]
pix2 = list()
for y in range(0, height2): #each pixel has coordinates
    row = ""
    for x in range(0, width2):

        RGB = img2.getpixel((x, y))
        pix2.append(RGB)

pix3 = list()
pix4 = list()
for i in range(0, pix1.__len__()):
    for j in range(0, 3):
        if pix1[i][j] != pix2[i][j]:
            pix3.append(pix1[i])
            pix4.append(pix2[i])
            break
with open("prithvi1.txt", "w") as f:
     f.write(str(pix3))

with open("prithvi2.txt", "w") as f1:
    f1.write(str(pix4))
