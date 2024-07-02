from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageSequence
import time
import numpy as np 
import random
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
        handle_img_gray(img,"000000","image")
    
def img_to_ascii(img:Image.Image, color:str,stype="image"):
    # finding depth by assigning ascii symbols to greyscale
    font = ImageFont.truetype("fonts/iosevka.ttf", 16)
    symbols = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    
    # symbols_small = "@%#*+=-:. "
    scale_dict = dict()
    for i in range(len(symbols)):
        # print(f"{symbols[i]} {font.getbbox(symbols[i])}")
        if i == len(symbols) - 1:
            scale_dict[255] = symbols[i]
        else:
            scale = int((225 / (len(symbols)-2) * i))
            scale_dict[scale] = symbols[i]
    vals = list(scale_dict.keys())
    mean = sum(font.getbbox(symbols[x])[3] for x in range(len(symbols))) // len(symbols)
    # print(mean)
    ## MAIN FUNCTION
    x,y = img.size
    if stype=="image":
        result = Image.new(mode="RGBA", size=((x),(y*8)), color="WHITE")
    else:
        result = open("res.txt", "w")

    draw = ImageDraw.Draw(result)
    
    data = np.asarray(img)
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
        if stype=="text":
            result.write(line)
            result.write('\n')
        else:
            if int(font.getlength(line)) > result.width:
            # print(f"{result.width}, {result.height}, {font.getlength(line)}")
                new = Image.new(mode="RGBA",size=(int(font.getlength(line)), result.height), color=f"#FFFFFF")
                new.paste(result, (0, 0))
                result = new.copy()
                draw = ImageDraw.Draw(result)
            draw.text(xy=(0, index_y*8), text=line, font=font, fill="#000000", anchor="lt")

        index_y+=1
    return result


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
        print(f"{len(frames)/img.n_frames * 100}%")
    frames[0].save("xd2.gif", save_all=True, append_images=frames[1:], duration=duration, loop=img.info['loop'])
   
   
def dithering(img: Image.Image, patternName:str):
    pattern = get_dither_algorithm(patternName)
    data = np.array(img, dtype=float) / 255 
    print(data.flags)
    for y in range(data.shape[0]-1):
        for x in range(data.shape[1]):
            old_val = data[y,x].copy()
            new_val = round(old_val)
            data[y,x] = new_val
            quant_error = old_val - new_val
    # DO ZMIANY
    #         quant_error = old_val - new_val
    #         if x < data.shape[1] - 1:
    #             data[y, x+1] += quant_error * 7 / div
    #         if y < data.shape[0] - 1:
    #             if x > 0:
    #                 data[y+1, x-1] += quant_error * 3/ div
    #             data[y+1,x] += quant_error * 5/ div
    #             if x < data.shape[1] - 1:
    #                 data[y+1,x+1] += quant_error * 1/ div
    # arr = np.array(data / np.max(data, axis=(0,1)) * 255, dtype=np.uint8)  
    # print(f"data:{data}\n max: {np.max(data, axis=(0,1))} arr: {arr}")          
    # result = Image.fromarray(arr)
    # result.save("algorithm.jpg")


    
   
## FUTURE FUNCTIONS FOR REFACTORING 
def handle_text(img:Image.Image, scale):
    pass # write res.txt

def get_dither_algorithm(algorithm:str): # can make this into a class in the future!!!!
    if algorithm == "f-s":
        pattern = np.array[[0,0,7],
                           [3,5,1]]
        pattern /= 16
    elif algorithm == "atkinson":
        pattern = np.array[[0,0,0,1,1],
                           [0,1,1,1,0],
                           [0,0,1,0,0]]
        pattern /= 8
    elif algorithm == "stucki":
        pattern = np.array[[0,0,0,8,4],
                           [2,4,8,4,2],
                           [1,2,4,2,1]]
        pattern /= 42
    elif algorithm == "sierra":
        pattern = np.array[[0,0,0,5,3],
                           [2,4,5,4,2],
                           [0,2,3,2,0]]
        pattern /= 32
    elif algorithm == "default":
        pattern = np.array()
        raise ValueError("Wrong algorithm!")
    return pattern

class Ditherer():
    pass #FUTURE

def img_to_braille(img:Image.Image):
    pass # text only for now

def handle_img_color(img:Image.Image, scale):
    pass # write res_rgb.png

def handle_img_gray(img:Image.Image, color,stype):
    if stype=="image":
        img = img_to_ascii(img,color,stype)
        img.save("res.png")
    

def text_to_ascii(mode):
    pass #future   
    
get_img("./src/pes10.png", 10)
end = time.time()
print(end-start)

