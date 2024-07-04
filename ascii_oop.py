from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageSequence
import time
import numpy as np 

class Ascii():
    def __init__(self, font_path,font_size):
        self.font_path = font_path
        self.font_size = font_size

    def img_to_ascii(self, img:Image.Image,color:str,stype:str):
        font = ImageFont.truetype(self.font_path,self.font_size)
        symbols = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
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
        x,y = img.size
        x_max = int(font.getlength(' ' * x))
        if stype=="image":
            result = Image.new(mode="RGBA", size=((x),(y*8)), color="WHITE")
            draw = ImageDraw.Draw(result)    
        else:
            result = ""
        data = np.asarray(img)
        closest = {}
        index_y = 0
        
        start = time.time()
        while index_y < y:
            index_x = 0
            line = ""
            while index_x < x:
                pxl = data[index_y,index_x]
                if pxl in closest.keys():
                    v = closest[pxl] ##bottleneck?
                else:
                    v = self.search(pxl, vals)
                    # v = symbols[pxl * (len(symbols) -1) // 255]
                    closest[pxl] = v
                line += scale_dict[v]
                # line += v
                index_x += 1
            starty = time.time() 
            if stype=="text":
                result+=line
                result+='\n'
            elif stype=="image":
                if int(font.getlength(line)) > result.width:
                # print(f"{result.width}, {result.height}, {font.getlength(line)}")
                    new = Image.new(mode="RGBA",size=(int(font.getlength(line)), result.height), color=f"#FFFFFF")
                    new.paste(result, (0, 0))
                    result = new.copy()
                    draw = ImageDraw.Draw(result)
                draw.text(xy=(0, index_y*8), text=line, font=font, fill=f"#000000", anchor="lt")
                endy = time.time()
                print(endy-starty)
            index_y+=1
        end = time.time()
        print(f"end:{end - start}")
        return result
    
    def search(self, x, A:list):
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
                    res = self.get_closest(A[mid -1], A[mid], x)
                    return res
                n = mid # mid się zmniejsza o mid ponieważ nic nie będzie mniejsze po prawej stronie
            else: # dla prawej strony
                if x < A[mid + 1] and mid < (n - 1): 
                    res = self.get_closest(A[mid + 1], A[mid], x)
                    return res
                i = mid + 1 # zwiększamy prawą stronę, i dąży do n

        return A[mid] #jeżeli nie zostanie nic
            
    def get_closest(self,a,b,x):
        if (a - x) <= (x - b):
            return a
        return b

class ImageHandler():
    def __init__(self,scale:int,font_path:str,stype:str,color:str="000000",font_size:int=16):
        self.scale=scale
        self.stype = stype
        self.color = color
        self.ascii = Ascii(font_path,font_size)
        
    def get_img(self, src:str):
        img = Image.open(src)
        img_format = img.format
        colorImg = img.copy()
        if img.format == "PNG":
            img = self.handle_png(img)
        img.format = img_format
        if img.format == "GIF":
            self.handle_gif(img)
        else:
            img = img.convert("L")
            img = img.resize((int(img.size[0]/self.scale), int(img.size[1]/self.scale)))
            res = self.ascii.img_to_ascii(img=img,color=f"#{self.color}",stype=self.stype)
            self.save_result(res=res)
            
            
    def handle_png(self,img):
        img_white = Image.new("RGBA", img.size, "WHITE")
        img_white.paste(img, (0, 0), img.convert("RGBA"))
        img = img_white
        return img

    def handle_gif(self, color, img):
        frames = []
        duration = []
        for frame in ImageSequence.Iterator(img):
            frame = frame.convert("L")
            frame = frame.resize((int(img.size[0]/self.scale), int(img.size[1]/self.scale)))
            frames.append(self.ascii.img_to_ascii(frame,color,stype="image"))
            duration.append(frame.info['duration'])
            print(f"{len(frames)/img.n_frames * 100}%")
        frames[0].save("result.gif", save_all=True, append_images=frames[1:], duration=duration, loop=img.info['loop'])
    
    def save_result(self,res):
        if self.stype == "image":
            res.save("result.png")
        elif self.stype == "text":
            with open("result.txt","w") as f:
                f.write(res)

if __name__ == "__main__":
    start = time.time()
    handler = ImageHandler(scale=2,font_path="./fonts/iosevka.ttf",stype="image",color="d00de3")  # Change to "image" to save as an image
    handler.get_img("src/cc.png")
    end = time.time()
    print(end - start)