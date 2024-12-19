import cv2
import pandas as pd

# Set the image path (update with the actual image file)
img_path = 'color/sample.jpg'  # Replace 'example.jpg' with your image path
img = cv2.imread(img_path)

# Global variables
clicked = False
r = g = b = xpos = ypos = 0

# Read CSV file
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('color/colors.csv', names=index, header=None)

# Function to find the closest color name
def getColorName(R, G, B):
    minimum = float('inf')
    cname = ''
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d < minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# Mouse callback function
def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        xpos, ypos = x, y
        b, g, r = img[y, x]
        b, g, r = int(b), int(g), int(r)

# Create a window and set a mouse callback
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:
    cv2.imshow("image", img)
    if clicked:
        # Draw a rectangle and display color information
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        text = getColorName(r, g, b) + f' R={r} G={g} B={b}'
        color = (255, 255, 255) if r + g + b < 600 else (0, 0, 0)
        cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA)
        clicked = False

    # Exit the loop when 'Esc' key is pressed
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()