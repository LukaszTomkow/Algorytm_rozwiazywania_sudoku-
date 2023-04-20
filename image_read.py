import pytesseract
import PIL.Image
import cv2

image_name = "sudoku.jpg"

myconfig = r"--psm 6 --oem 3"
text = pytesseract.image_to_string(PIL.Image.open(image_name), config = myconfig)
print(text)


img = cv2.imread(image_name)

basewidth = 600
tempimg = PIL.Image.open(image_name)
wpercent = (basewidth/float(tempimg.size[0]))
hsize = int((float(tempimg.size[1])*float(wpercent)))
tempimg = tempimg.resize((basewidth,hsize), PIL.Image.Resampling.LANCZOS)
tempimg.save(image_name)


height, width, _ = img.shape

boxes = pytesseract.image_to_boxes(img, config = myconfig)
for box in boxes.splitlines():
    box = box.split(" ")
    img = cv2.rectangle(img, (int(box[1]), height - int(box[2])), (int(box[3]), height - int(box[4])),(0,255,0), 2  )


cv2.imshow("img",img)
cv2.waitKey(0)

