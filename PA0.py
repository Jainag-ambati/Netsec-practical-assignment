from tkinter import *
from tkinter import Text

root=Tk()

canvas=Canvas(root,width=700,height=300)
canvas.pack()

lab1=Label(root,text="Practical Assignment-0",fg="black",font=('Arial',18))
lab1.place(relx=0.25,rely=0,relheight=0.2,relwidth=0.5)

l1=Label(root,text="Plaintext",fg="black",font=('Verdana',11))
l1.place(relx=0,rely=0.16,relheight=0.1,relwidth=0.5)

l2=Label(root,text="Ciphertext",fg="black",font=('Verdana',11))
l2.place(relx=0.5,rely=0.16,relheight=0.1,relwidth=0.5)

#plaintext box
e1=Entry(root,fg="red",bg="yellow",border=5,font=('Arial',16))
e1.place(relx=0.02,rely=0.25,relheight=0.1,relwidth=0.4)


lab=Label(root,text="<---->")
lab.place(relx=0.45,rely=0.25,relheight=0.1,relwidth=0.1)

#ciphertext box
e2=Entry(root,fg="blue",bg="yellow",border=5,font=('Arial',16))
e2.place(relx=0.58,rely=0.25,relheight=0.1,relwidth=0.4)

dic= {'a':'z','b':'y','c':'x','d':'w','e':'v','f':'u','g':'t','h':'s','i':'r','j':'q',
          'k':'p',
          'l':'o',
          'm':'n',
          'n':'m',
          'o':'l',
          'p':'k',
          'q':'j',
          'r':'i',
          's':'h',
          't':'g',
          'u':'f',
          'v':'e',
          'w':'d',
          'x':'c',
          'y':'b',
          'z':'a',
          'A':'Z',
          'B':'Y',
          'C':'X',
          'D':'W',
          'E':'V',
          'F':'U',
          'G':'T',
          'H':'S',
          'I':'R',
          'J':'Q',
          'K':'P',
          'L':'O',
          'M':'N',
          'N':'M',
          'O':'L',
          'P':'K',
          'Q':'J',
          'R':'I',
          'S':'H',
          'T':'G',
          'U':'F',
          'V':'E',
          'W':'D',
          'X':'C',
          'Y':'B',
          'Z':'A',
          ' ':' '
         }
#enciphering function
def fun1():
    text=e1.get()
    res=""
    for k in text:
        res=res+dic[k]
    e2.delete(0,END)    
    e2.insert(0,res)

#deciphering function
def fun2():
    text=e2.get()
    res=""
    for k in text:
        res=res+dic[k]
    e1.delete(0,END)    
    e1.insert(0,res)
    
#button to encipher the plaintext to ciphertext
but1=Button(root,text="ENCRYPT",command=fun1,bg="green")
but1.place(relx=0.07,rely=0.4,relheight=0.07,relwidth=0.3)

#button to decipher the ciphertext to plaintext
but2=Button(root,text="DECRYPT",command=fun2,bg="red")
but2.place(relx=0.63,rely=0.4,relheight=0.07,relwidth=0.3)

lab2=Label(root,text="AMBATI JAINAG",fg="black",font=('Verdana',12))
lab2.place(relx=0.3,rely=0.6,relheight=0.06,relwidth=0.4)
lab3=Label(root,text="18095012",fg="black",font=('Verdana',12))
lab3.place(relx=0.31,rely=0.66,relheight=0.06,relwidth=0.4)
lab4=Label(root,text="Electronics Dept",fg="black",font=('Verdana',12))
lab4.place(relx=0.3,rely=0.72,relheight=0.06,relwidth=0.4)

root.mainloop()
 
