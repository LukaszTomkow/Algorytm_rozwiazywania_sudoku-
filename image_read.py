import pytesseract
import PIL.Image
import cv2
import numpy as np

def extract_sudoku_cells(sudoku_grid):
    cell_height = sudoku_grid.shape[0] // 9
    cell_width = sudoku_grid.shape[1] // 9
    cells = []
    for row in range(9):
        for col in range(9):
            cell_y = row * cell_height + cell_height // 9
            cell_x = col * cell_width + cell_width // 9
            cell_h = cell_height - cell_height // 9
            cell_w = cell_width - cell_width // 9
            cell = sudoku_grid[cell_y:cell_y+cell_h, cell_x:cell_x+cell_w]
            cells.append(cell)
    return cells


image_name = "przechwytywanie.png"

# Przygotowanie obrazka
img = cv2.imread(image_name)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(img, (3, 3), 0)
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Wyodrębnienie siatki Sudoku
edges = cv2.Canny(thresh, 50, 150)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contour = max(contours, key=cv2.contourArea)
epsilon = 0.05 * cv2.arcLength(contour, True)
approx = cv2.approxPolyDP(contour, epsilon, True)
x, y, w, h = cv2.boundingRect(approx)
sudoku_grid = thresh[y:y+h, x:x+w]

# Wyodrębnienie komórek Sudoku
cells = extract_sudoku_cells(sudoku_grid)

# Ustawienia Tesseract
#myconfig = r"--psm 10 digits --oem 3 -c tessedit_char_whitelist=123456789"
myconfig = r"--psm 10 digits --oem 3"# -c tessedit_char_whitelist=123456789"

# Przetwarzanie komórek i wykonywanie OCR
extracted_text = []

for cell in cells:
    text = pytesseract.image_to_string(PIL.Image.fromarray(cell), config=myconfig)
    #print(text)
    #cv2.imshow("Digit", cell)
    #cv2.waitKey(1)
    if text.strip().isdigit():
        extracted_text.append(int(text.strip()))
    else:
        extracted_text.append("")

# Przekształcenie tekstu
#processed_text = ''
#for text in extracted_text:
#    if text.isdigit():
#        processed_text += text
#    else:
#        processed_text += ' '

# Sprawdzenie, czy otrzymany tekst składa się z 81 cyfr
if len(extracted_text) == 81:
    sudoku_board = np.array([ "" if isinstance(digit, str) else int(digit) for digit in extracted_text]).reshape((9, 9))
    print(sudoku_board)
else:
    print("Błąd: Nieprawidłowa liczba cyfr Sudoku")
