from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy
import time


collection = []
feature_vector = {}


def threshold(pix):
    if pix >= 128:
        return 1
    else:
        return 0


img = Image.open('skeleton_new.tif', 'r')
pix_vals = list(img.getdata())

isolate_point = 0
ridge_ending = 0
continuing_ridge = 0
bifurcation_point = 0
crossing_point = 0

for i in range(0, pix_vals.__len__()):
    pix_vals[i] = threshold(pix_vals[i])


new_pix = list()
new_pix1 = list()
for i in pix_vals:
    new_pix.append(i)

new_pix1.append(new_pix[0])
for i in range(0, 388):
    new_pix1.append(new_pix[i])
new_pix1.append(new_pix[387])

k = 0
for j in range(0, 374):
    new_pix1.append(new_pix[j*388])
    for i in range(0, 388):
        new_pix1.append(new_pix[k])
        k += 1
    new_pix1.append(new_pix[(j+1)*387])

new_pix1.append(new_pix[373*388])
for i in range(0, 388):
    new_pix1.append(new_pix[i])
new_pix1.append(new_pix[374*387])
avg = 0
new_pix2 = list()

a = list()
q = 0
for i in range(0, 376):
    b = list()
    for j in range(0, 390):
        b.append(new_pix1[q])
        q += 1
    a.append(b)
start = time.time()
for i in range(1, 375):
    for j in range(1, 389):
        sum = 0
        if a[i][j] == 1:
            sum += (abs(a[i-1][j-1]-a[i][j-1])+abs(a[i][j-1]-a[i+1][j-1])+abs(a[i+1][j-1]-a[i+1][j])+abs(a[i+1][j]-a[i+1][j+1])+abs(a[i+1][j+1]-a[i][j+1])+abs(a[i][j+1]-a[i-1][j+1])+abs(a[i-1][j+1]-a[i-1][j])+abs(a[i-1][j]-a[i-1][j-1]))/2
            if sum == 0:
                isolate_point += 1
                feature_vector = {"position_x": i, "position_y": j, "type": "isolate_point"}
            elif sum == 1:
                ridge_ending += 1
                feature_vector = {"position_x": i, "position_y": j, "type": "ridge_ending"}
            elif sum == 2:
                continuing_ridge += 1
                feature_vector = {"position_x": i, "position_y": j, "type": "continuing_ridge"}
            elif sum == 3:
                bifurcation_point += 1
                feature_vector = {"position_x": i, "position_y": j, "type": "bifurcation_point"}
            elif sum == 4:
                crossing_point += 1
                feature_vector = {"position_x": i, "position_y": j, "type": "crossing_point"}
            collection.append(feature_vector)
stop = time.time()
print("ISOLATE POINTS : ", isolate_point)
print("RIDGE ENDING POINTS : ", ridge_ending)
print("CONTINUING RIDGE POINTS : ", continuing_ridge)
print("BIFURCATION POINTS : ", bifurcation_point)
print("CROSSING POINTS : ", crossing_point)

print("Total Sum : ", isolate_point+ridge_ending+continuing_ridge+bifurcation_point+crossing_point)

print("Time taken : ", stop-start)
#
# img = Image.open('101_1.tif', 'r')
# img1 = Image.open('skeleton_new.tif', 'r')
# fig, (ax0, ax1) = plt.subplots(1, 2)
# ax0.imshow(img, cmap='gray')
# ax0.axis('off')
# ax0.set_title('Original Image')
# ax1.imshow(img1, cmap='gray')
# ax1.axis('off')
# ax1.set_title('Skeleton')
# plt.show()
# for i in collection:
#     print(i)

with open("Feature_Vector.txt", "w") as f:
    for fv in collection:
        f.write(str(fv))
        f.write("\n")



