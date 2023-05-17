import pytesseract
import PIL.Image
import cv2

image_name = "sudoku.jpg"


# Przygotowanie obrazka
img = cv2.imread(image_name)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
img = cv2.imread(image_name)
basewidth = 600
tempimg = PIL.Image.open(image_name)
wpercent = (basewidth/float(tempimg.size[0]))
hsize = int((float(tempimg.size[1])*float(wpercent)))
tempimg = tempimg.resize((basewidth,hsize), PIL.Image.Resampling.LANCZOS)
tempimg.save(image_name)
height, width, _ = img.shape


#boxes = pytesseract.image_to_boxes(img, config = myconfig)
#for box in boxes.splitlines():
#    box = box.split(" ")
#    img = cv2.rectangle(img, (int(box[1]), height - int(box[2])), (int(box[3]), height - int(box[4])),(0,255,0), 2  )
#cv2.imshow("img",img)
#cv2.waitKey(0)


# Ustawienia Tesseract
myconfig = r"--psm 6 --oem 3"
# Wykonanie OCR na przetworzonym obrazku
text = pytesseract.image_to_string(PIL.Image.open(image_name), config = myconfig)
print(text)

# Przekształcenie tekstu
processed_text = ''.join([c for c in text if c.isdigit()])  # Usunięcie wszystkich znaków, oprócz cyfr


print(processed_text)