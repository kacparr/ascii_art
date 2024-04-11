from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageSequence
import time
import numpy as np 
start = time.time()
def get_img(src, scale:int=1): # MODE
    ## opening the image
    img = Image.open(src)
    img_format = img.format
    colorImg = img.copy()
    if img.format == "PNG":
        img_white = Image.new("RGBA", img.size, "WHITE")
        img_white.paste(img, (0, 0), img.convert("RGBA"))
        img = img_white
    img.format = img_format
    if img.format == "GIF":
        handle_gif(img, scale)
    else:
        img = img.convert("L")
        img = img.resize((int(img.size[0]/scale), int(img.size[1]/scale)))
        img_to_ascii(img)
    
def img_to_ascii(img:Image.Image):
    # finding depth by assigning ascii symbols to greyscale
    font = ImageFont.truetype("fonts/firamono.ttf", 16)
    symbols = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    # symbols_small = "@%#*+=-:. "
    scale_dict = dict()
    for i in range(len(symbols)):
        print(f"{symbols[i]} {font.getbbox(symbols[i])}")
        if i == len(symbols) - 1:
            scale_dict[255] = symbols[i]
        else:
            scale = int((225 / (len(symbols)-2) * i))
            scale_dict[scale] = symbols[i]
    vals = list(scale_dict.keys())
    ## MAIN FUNCTION
    x,y = img.size
    result = Image.new(mode="RGBA", size=((x),(y*8)), color="WHITE")

    draw = ImageDraw.Draw(result)
    
    data = np.asarray(img)
    res = open("res.txt", "w")
    closest = {}
    index_y = 0
    while index_y < y:
        index_x = 0
        line = ""
        while index_x < x: 
            pxl = data[index_y,index_x]
            if pxl in closest.keys():
                v = closest[pxl] ##bottleneck?
            else:
                v = search(pxl, vals)
                # v = symbols[pxl * (len(symbols) -1) // 255]
                closest[pxl] = v
            line += scale_dict[v]
            # line += v
            index_x += 1
        res.write(line)
        if int(font.getlength(line)) > result.width:
            # print(f"{result.width}, {result.height}, {font.getlength(line)}")
            new = Image.new(mode="RGBA",size=(int(font.getlength(line)), result.height), color="#ffffff")
            new.paste(result, (0, 0))
            result = new.copy()
            draw = ImageDraw.Draw(result)
        draw.text(xy=(0, index_y*8), text=line, font=font, fill="#000000", anchor="lt")

        res.write('\n')
        index_y+=1
    result.save("res.png")

def search(x, A:list):
    #1. Dzielenie listy na 3 do optymalizacji
    A_i = ((0,9), (10,39), (40,70))
    x_mod = x // 100
    A = A[A_i[x_mod][0]:A_i[x_mod][1]]
    # i = prawa strona, mid dzieli array na 2, n = długość arraya
    i, mid, n = 0, 0, len(A)
    # sprawdzanie pierwszego i ostatniego indeksu
    if x <= A[0]:
        return A[0]
    if x >= A[n-1]:
        return A[n-1]
    while i < n:
        mid = (i + n) // 2
        if x == A[mid]:
            return A[mid]

        if x < A[mid]: # dla lewej strony
            if x > A[mid - 1] and mid > 0:
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

    
def handle_gif(img:Image.Image, scale): #color or not?
    frames = []
    duration = []
    for frame in ImageSequence.Iterator(img):
        frame = frame.convert("L")
        frame = frame.resize((int(img.size[0]/scale), int(img.size[1]/scale)))
        frames.append(img_to_ascii(frame))
        duration.append(frame.info['duration'])
        print(len(frames))
    frames[0].save("xd2.gif", save_all=True, append_images=frames[1:], duration=duration, loop=img.info['loop'])
   
   
## FUTURE FUNCTIONS FOR REFACTORING 
def handle_text(img:Image.Image, scale):
    pass # write res.txt

def handle_img_color(img:Image.Image, scale):
    pass # write res_rgb.png

def handle_img_gray(img:Image.Image, scale):
    pass # write res.png 

def text_to_ascii(mode):
    pass #future   
    
get_img("src/image.jpg", 2)
end = time.time()
print(end-start)

