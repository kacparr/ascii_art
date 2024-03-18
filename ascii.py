# TODO
# Image scaling, right now 1 letter = 1 pixel, the goal is to change it to e.g 4 pixels
# Moving the text into image (finding the right size etc) if image scaling will be implemented
# Coloring the letters if text is moved 
# Trying to show the art in terminal if that will work
# Making the function to auto-generate ASCII letters in different styles

from PIL import Image, ImageColor, ImageDraw, ImageFont
import time

start = time.time()
def img_to_ascii():
    img = Image.open("d.jpg")
    colorImg = img.copy()
    img = img.convert("LA")
    _x,_y = img.size
    img = img.resize((int(_x-0*_x), int(_y-0*_y)))
    x,y = img.size

    newImg = Image.new(mode="RGBA", size=(x*2,y*2), color=(255,0,0,0))
    font = ImageFont.truetype("iosevka.ttf",6)
    draw = ImageDraw.Draw(newImg)

    with open("symbols.txt", "r") as s:
        symbols = list(s.read())

    scale_dict = dict()
    for i in range(len(symbols) -1, -1, -1):
        if i == 69:
            scale_dict[255] = symbols[i]
        else:
            scale = int((235 / 68) * i)
            scale_dict[scale] = symbols[i]
    print(scale_dict)
    vals = list(scale_dict.keys())

    # print(vals)
    closest = {}
    res = open("res.txt", "w")
    for i in range(y):
        for j in range(x):
            p = img.getpixel((j,i))[0]
            if p in closest.keys():
                v = closest[p]
            else:
                v = search(p, vals)
                # print(f"pixel:{p}. closest:{v}")
                closest[p] = v
            res.write(scale_dict[v])
            draw.text(xy=(j*2,i*2),text=scale_dict[v],font=font)
        res.write('\n')
    newImg.save("xd.png")



                

def search(x, A:list):
    #1. Dzielenie listy na 3 do optymalizacji
    A_i = ((40,70), (10,39), (0,9))
    x_mod = x // 100
    A = A[A_i[x_mod][0]:A_i[x_mod][1]]
    A.reverse()
    # print(A)
    # i = prawa strona, mid dzieli array na 2, n = długość arraya
    i, mid, n = 0, 0, len(A)
    # sprawdzanie pierwszego i ostatniego indeksu
    if x <= A[0]:
        return A[0]
    if x >= A[n-1]:
        return A[n-1]
    while i < n:
        mid = (i + n) // 2
        # print(f"mid: {mid}, x={x}, n={n}")
        # jeżeli idealnie mid
        if x == A[mid]:
            return A[mid]

        if x < A[mid]: # dla lewej strony
            if x > A[mid - 1] and mid > 0:
                # print(A[mid-1], A[mid], x)
                res = get_closest(A[mid -1], A[mid], x)
                return res
            n = mid # mid się zmniejsza o mid ponieważ nic nie będzie mniejsze po prawej stronie
        else: # dla prawej strony
            if x < A[mid + 1] and mid < (n - 1): 
                res = get_closest(A[mid + 1], A[mid], x)
                return res
            i = mid + 1 # zwiększamy prawą stronę, i dąży do n
        
    return A[mid] #jeżeli nie zostanie nic
        
def get_closest(a,b,x):
    if (a - x) <= (x - b):
        return a
    return b

img_to_ascii()
end = time.time()
print(end-start)