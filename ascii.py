from PIL import Image, ImageColor, ImageDraw, ImageFont
import time
import numpy as np 
start = time.time()
def img_to_ascii():
    symbols = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    symbols_short = "@%#*+=-:. "
    ## opening the image
    img = Image.open("src/sand.png")
    colorImg = img.copy()
    img_white = Image.new("RGBA", img.size, "WHITE")
    img_white.paste(img, (0, 0), img)
    img = img_white
    img.save("ahaha.png")
    img = img.convert("L")
    img = img.resize((int(img.size[0]), int(img.size[1])))
    x,y = img.size
    newImg = Image.new(mode="RGBA", size=((x*4)-1,(y*4)-1), color=(255,0,0,0))
    font = ImageFont.truetype("iosevka.ttf",8) ## find em 

    # finding depth by assigning ascii symbols to the greyscale
    scale_dict = dict()
    for i in range(len(symbols)):
        if i == 69:
            scale_dict[255] = symbols[i]
        else:
            scale = int((235 / (len(symbols)-2) * i))
            scale_dict[scale] = symbols[i]
    # print(scale_dict)
    vals = list(scale_dict.keys())
    ## MAIN FUNCTION
    data = np.asarray(img)
    print(data)
    res = open("res.txt", "w")
    closest = {}
    index_y = 0
    while index_y < y:
        index_x = 0
        line = ""
        while index_x < x: 
            pxl = data[index_y,index_x]
            # print(colors)
                ## convert
            if pxl in closest.keys():
                v = closest[pxl] ##bottleneck?
            else:
                v = search(pxl, vals)
                closest[pxl] = v
            res.write(scale_dict[v])
            line += scale_dict[v]
            index_x += 1
        res.write('\n')
        index_y+=1

    # # print(vals)
    # for i in range(y):
    #     for j in range(x):
    #         p = img.getpixel((j,i))[0]

    #         else:
    #             v = search(p, vals)
    #             # print(f"pixel:{p}. closest:{v}")
    #             closest[p] = v
    #         res.write(scale_dict[v])
    #         draw.text(xy=(j*4,i*4),text=scale_dict[v],font=font, fill="#000000")
    #     res.write('\n')
    # newImg.save("xd.png")

def search(x, A:list):
    #1. Dzielenie listy na 3 do optymalizacji
    A_i = ((0,9), (10,39), (40,70))

    x_mod = x // 100
    A = A[A_i[x_mod][0]:A_i[x_mod][1]]

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
            