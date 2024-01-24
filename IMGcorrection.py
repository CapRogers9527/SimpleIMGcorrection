import cv2
import numpy as np

def get_size(path):
    image = cv2.imread(path)
    height, width = image.shape[:2]
    return height, width


def perspective_transform(image, a1, b1, a2, b2, a3, b3, a4, b4):
    # input four points
    src_points = np.float32([[a1, b1], [a2, b2], [a3, b3], [a4, b4]])
    
    # connors
    dst_points = np.float32([[0, 0], [image.shape[1], 0], [image.shape[1], image.shape[0]], [0, image.shape[0]]])

    # get perspective transform martix
    M = cv2.getPerspectiveTransform(src_points, dst_points)

    result = cv2.warpPerspective(image, M, (image.shape[1], image.shape[0]))
    cv2.imshow('Original Image', image)
    cv2.imshow('Corrected Image', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def find_connorPoints(corner_array):
    
    h,w = get_size(image_path)
    print(h,w)
    leng = len(corner_array)
    print(leng)
    minds = 1000000000000000
    mina = 1000000000000000
    minb = 1000000000000000
    py = [0,w,w,0]
    px = [0,0,h,h]
    ansx=[0,0,0,0]
    ansy=[0,0,0,0]
    for k in range(4):
        for j in range(leng):
            #print(str(corner_array[j]))
            #print(len(str(corner_array[i])))
            for i in range(len(str(corner_array[j]))):
                if (str(corner_array[j])[i:i+1]==' '):
                    index = i
            a = int(str(corner_array[j])[1:index])
            b = int(str(corner_array[j])[index:len(str(corner_array[j]))-1])
            #print(str(a)+'-'+str(b))
            dis = abs(a-px[k]) + abs(b-py[k])
            #print(dis)
            if dis < minds:
                minds = dis
                mina = a
                ansx[k] = a
                minb = b
                ansy[k] = b
        print(str(mina)+'&'+str(minb))
        minds = 1000000000000000
        mina = 1000000000000000
        minb = 1000000000000000
    return ansx,ansy


def save_harris_corners(image_path):

    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # calcualte all harris points
    corners = cv2.cornerHarris(gray, 2, 3, 0.04)

    image_with_corners = image.copy()
    image_with_corners[corners > 0.01 * corners.max()] = [0, 0, 255]  # 将角点标记为红色

    corner_coordinates = np.column_stack(np.where(corners > 0.01 * corners.max()))

    corner_array = np.array(corner_coordinates)
    print("All Corner Coordinates:")
    #print(corner_array)
    xx,yy=find_connorPoints(corner_array)
    perspective_transform(image, yy[0], xx[0],yy[1], xx[1], yy[2], xx[2], yy[3], xx[3])

    cv2.imshow('Harris Corners', image_with_corners)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return corner_array

if __name__ == "__main__":
    image_path = "check.jpg"
    corners_array = save_harris_corners(image_path)


