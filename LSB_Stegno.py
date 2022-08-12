# import modules
from tkinter import *
import tkinter.filedialog           #This module is used to work with files
from tkinter import messagebox      #For showing messages on the screen
from PIL import Image
from io import BytesIO
import os                           #Used for creating and removing any directory


class IMG_Stegno:
    output_image_size = 0

    # Main frame or start page
    def main(self, root):

        #Initializing the root window
        root.title('ImageSteganography')
        root.geometry('400x400')
        #root.resizable(width=False, height=False)
        root.config()
        frame = Frame(root)
        frame.grid()

        title = Label(frame, text='LSB Image Steganography')
        title.config(font=('Times new roman', 25, 'bold'))
        title.grid(pady=10)
        title.config()
        title.grid(row=1)

        encode = Button(frame, text="Encode", command=lambda: self.encode_frame1(frame), padx=14)
        encode.config(font=14, bg='light blue')
        encode.grid(pady=12)
        encode.grid(row=2)

        decode = Button(frame, text="Decode", command=lambda: self.decode_frame1(frame), padx=14)
        decode.config(font=14, bg='light blue')
        decode.grid(pady=12)
        decode.grid(row=3)

        exit = Button(frame, text="Exit", command=lambda: self.exit(frame), padx=14)
        exit.config(font=14, bg='light blue')
        exit.grid(pady=12)
        exit.grid(row=4)

        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

    # Back function to loop back to main screen
    def back(self, frame):
        frame.destroy()
        self.main(root)

    # Frame for encode page
    def encode_frame1(self, frame):
        frame.destroy()
        e_f2 = Frame(root)
        label1 = Label(e_f2, text='Select the Image in which \nyou want to hide text :')
        label1.config(font=('Times new roman', 25, 'bold'))
        label1.grid()

        button_bws = Button(e_f2, text='Select', command=lambda: self.encode_frame2(e_f2))
        button_bws.config(font=20, bg='light blue')
        button_bws.grid()

        button_back = Button(e_f2, text='Cancel', command=lambda: IMG_Stegno.back(self, e_f2))
        button_back.config(font=20, bg='light blue')
        button_back.grid(pady=15)
        button_back.grid()
        e_f2.grid()

    # Frame for decode page
    def decode_frame1(self, F):
        F.destroy()
        d_f2 = Frame(root)
        label1 = Label(d_f2, text='Select Image with \nHidden text:')
        label1.config(font=('Times new roman', 25, 'bold'))
        label1.grid()
        label1.config()
        button_bws = Button(d_f2, text='Select', command=lambda: self.decode_frame2(d_f2))
        button_bws.config(font=20, bg='light blue')
        button_bws.grid()
        button_back = Button(d_f2, text='Cancel', command=lambda: IMG_Stegno.back(self, d_f2))
        button_back.config(font=20, bg='light blue')
        button_back.grid(pady=15)
        button_back.grid()
        d_f2.grid()

    # Function to encode image
    def encode_frame2(self, e_F2):
        e_pg = Frame(root)
        myfile = tkinter.filedialog.askopenfilename(filetypes=([('png', '*.png'), ('jpeg', '*.jpeg'), ('jpg', '*.jpg'), ('All Files', '*.*')]))
        if not myfile:
            messagebox.showerror("Error", "You have selected nothing !")
        else:
            my_img = Image.open(myfile)
            label2 = Label(e_pg, text='Enter the message')
            label2.config(font=('Helvetica', 14, 'bold'))
            label2.grid(pady=15)
            text_a = Text(e_pg, width=40, height=10)
            text_a.grid()
            encode_button = Button(e_pg, text='Cancel', command=lambda: IMG_Stegno.back(self, e_pg))
            encode_button.config(font=('Helvetica', 14), bg='light blue')
            data = text_a.get("1.0", "end-1c")
            button_back = Button(e_pg, text='Encode', command=lambda: [self.enc_fun(text_a, my_img), IMG_Stegno.back(self, e_pg)])
            button_back.config(font=('Helvetica', 14), bg='light blue')
            button_back.grid(pady=15)
            encode_button.grid()
            e_pg.grid(row=1)
            e_F2.destroy()

    # Function to decode image
    def decode_frame2(self, d_F2):
        d_F3 = Frame(root)
        myfiles = tkinter.filedialog.askopenfilename(
            filetypes=([('png', '*.png'), ('jpeg', '*.jpeg'), ('jpg', '*.jpg'), ('All Files', '*.*')]))
        if not myfiles:
            messagebox.showerror("Error", "You have selected nothing! ")
        else:
            my_img = Image.open(myfiles, 'r')
            hidden_data = self.decode(my_img)
            label2 = Label(d_F3, text='Hidden data is :')
            label2.config(font=('Helvetica', 14, 'bold'))
            label2.grid(pady=10)
            text_a = Text(d_F3, width=40, height=10)
            text_a.insert(INSERT, hidden_data)
            text_a.configure(state='disabled')
            text_a.grid()
            button_back = Button(d_F3, text='Cancel', command=lambda: self.frame_3(d_F3))
            button_back.config(font=('Helvetica', 14), bg='light blue')
            button_back.grid(pady=15)
            button_back.grid()
            d_F3.grid(row=1)
            d_F2.destroy()

    # Function to decode data
    def decode(self, image):
        image_data = iter(image.getdata())
        data = ''

        while (True):
            pixels = [value for value in image_data.__next__()[:3] +
                      image_data.__next__()[:3] +
                      image_data.__next__()[:3]]
            binary_str = ''
            for i in pixels[:8]:
                if i % 2 == 0:
                    binary_str += '0'
                else:
                    binary_str += '1'

            data += chr(int(binary_str, 2))
            if pixels[-1] % 2 != 0:
                return data

    # Function to generate data
    def generate_Data(self, data):
        new_data = []

        for i in data:
            new_data.append(format(ord(i), '08b'))
        return new_data

    # Function to modify the pixels of image
    def modify_Pix(self, pix, data):
        dataList = self.generate_Data(data)
        dataLen = len(dataList)
        imgData = iter(pix)
        for i in range(dataLen):

            pix = [value for value in imgData.__next__()[:3] +
                   imgData.__next__()[:3] +
                   imgData.__next__()[:3]]

            for j in range(0, 8):
                if (dataList[i][j] == '0') and (pix[j] % 2 != 0):
                    if (pix[j] % 2 != 0):
                        pix[j] -= 1

                elif (dataList[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1

            if (i == dataLen - 1):
                if (pix[-1] % 2 == 0):
                    pix[-1] -= 1
            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1

            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    # Function to enter the data pixels in image
    def encode_enc(self, newImg, data):
        w = newImg.size[0]
        (x, y) = (0, 0)

        for pixel in self.modify_Pix(newImg.getdata(), data):

            # Putting modified pixels in the new image
            newImg.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1

    # Function to enter hidden text
    def enc_fun(self, text_a, myImg):
        data = text_a.get("1.0", "end-1c")
        if (len(data) == 0):
            messagebox.showinfo("Alert", "Kindly enter text in TextBox")
        else:
            newImg = myImg.copy()
            self.encode_enc(newImg, data)
            my_file = BytesIO()
            temp = os.path.splitext(os.path.basename(myImg.filename))[0]
            newImg.save(tkinter.filedialog.asksaveasfilename(initialfile=temp, filetypes=([('png', '*.png')]),
                                                             defaultextension=".png"))
            # self.d_image_size = my_file.tell()
            # self.d_image_w, self.d_image_h = newImg.size
            messagebox.showinfo("Success",
                                "Encoding Successful\nFile is saved in the same directory")

    def frame_3(self, frame):
        frame.destroy()
        self.main(root)

    def exit(self,frame):
        frame.quit()


# GUI loop
root = Tk()
o = IMG_Stegno()
o.main(root)
root.mainloop()