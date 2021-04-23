import matplotlib.pyplot as plt
from tkinter import *
from tkinter import Text
from PIL import ImageTk, Image
from binascii import hexlify, unhexlify
from random import *
from typing import List, Tuple


def apply_permutation(s: str, vec: List[int], sz: int):
  """We can apply a specific permutation to a string in different rounds of DES"""
  res = ""
  for i in range(sz):
    res += s[vec[i] - 1]
  return res

def calculatexor(s1: str, s2: str):
  """Calculates xor in position wise manner in both strings s1 and s2"""
  res = ""
  for i in range(len(s1)):
    if (s1[i] == s2[i]):
      res += '0'
    else:
      res += '1'
  return res


def calc_diff(vec1: List[List[str]], vec2: List[List[str]]):
  """ This is used for plotting the avalanche effect induced during each round of DES.
This function calculates number of bits that are different between two ciphertexts"""
  change = []
  len1=len(vec1[0])
  len2=len(vec1)
  for i in range(len1):
    a=0
    for j in range(len2):
      for (bit1,bit2) in zip(vec1[j][i], vec2[j][i]):
        if(bit1 != bit2):
          a=a+1
    change.append(a)
  return change



def change_text(txt: str, n: int) -> str:
  """Toggles the 'n' number of positions in the given txt(bin)"""
  length = len(txt)
  vec = sample(range(0,length),n)
  vec.sort() 
  new_txt = ""
  i = 0
  #Toggling process
  for pos in vec:
    new_txt += txt[i:pos]
    i = pos+1
    if(txt[pos] == '1'):
      new_txt += '0'
    else:
      new_txt += '1'
  
  new_txt += txt[i:]
  return new_txt


def round_keys_generator(key: str, rounds: int =16, half_width: int =32):
  """Generates the Round keys for DES given appropriate binary key string,
     number of rounds to be used in DES and the halfwidth of the plaintext.
     Returns a list of round keys in binary format."""
 

  if(half_width == 32):
    # Standard Permuted Choice-1
    PC_1 = [ 57, 49, 41, 33, 25, 17, 9, 
            1, 58, 50, 42, 34, 26, 18, 
            10, 2, 59, 51, 43, 35, 27, 
            19, 11, 3, 60, 52, 44, 36, 
            63, 55, 47, 39, 31, 23, 15, 
            7, 62, 54, 46, 38, 30, 22, 
            14, 6, 61, 53, 45, 37, 29, 
            21, 13, 5, 28, 20, 12, 4 ]
    # Standard Permuted Choice-2
    PC_2 = [ 14, 17, 11, 24, 1, 5, 
            3, 28, 15, 6, 21, 10, 
            23, 19, 12, 4, 26, 8, 
            16, 7, 27, 20, 13, 2, 
            41, 52, 31, 37, 47, 55, 
            30, 40, 51, 45, 33, 48, 
            44, 49, 39, 56, 34, 53, 
            46, 42, 50, 36, 29, 32 ]
  else:
    #we have to generate Permuted Choice-1 array and Permuted Choice-2 array of a given size
    arr = [x for x in range(1,2*half_width+1) if x%8 != 0]
    seed(99)
    shuffle(arr)

    PC_1 = arr
    var1=len(PC_1)
    var2=(half_width)//4

    seed(99)
    pos = sample(range(var1),var2)
    arr = []
    for i in range(var1):
      if(i not in pos):
       arr.append(i+1)
    seed(99)
    shuffle(arr)
  
    PC_2 = arr
      
  # Applying permuted choice-1 for dropping the parity bits in the key
  key = apply_permutation(key, PC_1, len(PC_1))

  # Splitting the key
  half = len(key)//2
  left = key[0:half]
  right = key[half:]
  
  # RoundKeys in binary format
  roundk_bin = []
 
  shift_table = [ 1, 1, 2, 2, 2, 2, 2, 2,1, 2, 2, 2, 2, 2, 2, 1 ]
  for i in range(rounds): 
    # need to use above shift_table which is standard for rounds less than or equal to 16
    if(i < 16): 
      left = left[shift_table[i]:] + left[:shift_table[i]]
      right = right[shift_table[i]:] + right[:shift_table[i]]
    else: # Use a shift of 2 for rounds more than 16
      left = left[2:] + left[:2]
      right = right[2:] + right[:2]

    total = left + right 

    # compressing the key 
    RoundKey = apply_permutation(total, PC_2, len(PC_2))
    roundk_bin.append(RoundKey)
   
  
  return roundk_bin

def desalgo(plaintext: str, key: str, rounds: int =16, half_width: int =32, bp: int =0,  bk: int=0) :
  #bp=no of bits in plaintext to be changed for observing avalanche affect
  #bk=no of bits in key to be changed for observing avalanche affect

  #converting given plaintext into hexadecimal format
  plaintext = hexlify(plaintext.encode()).decode()

  #converting hexadecimal plaintext into binary format
  plaintext = bin(int(plaintext,16))[2:]
  
  #converting given key into hexadecimal format
  #key = hexlify(key.encode()).decode()

  #converting hexadecimal key into binary format
  #key = bin(int(key,16))[2:]

  #dividing the complete binary plaintext into blocks of length 2*half_width
  length = 2*half_width
  x = len(plaintext)%length
  if(x != 0):
    x = length - x
  plaintext = '0'*x + plaintext

  if(bp != 0):
    plaintext = change_text(plaintext,bp)
  pt_blocks = []
  i=0
  while(i+length <= len(plaintext)):
    pt_blocks.append(plaintext[i:i+length])
    i += length

  #now structuring the key
  if(len(key) > 2*half_width):
    key = key[:2*half_width]
  key = key.zfill(2*half_width)

  if(bk != 0):
    key = change_text(key,bk)


  
  roundk_bin= round_keys_generator(key, rounds, half_width)

  # intializing standard s-box for DES
  s_box = [
          [ 
            [ 14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7], 
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8], 
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0], 
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
          ], 
          [ 
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10], 
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
          ], 
          [ 
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12 ]
          ],
          [ 
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15], 
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4], 
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14 ]
          ], 
          [ 
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3 ]
          ],
          [ 
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11], 
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8], 
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13 ]
          ], 
          [ 
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12 ]
          ],
          [ 
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7], 
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11] 
          ]
      ]    
  
  if(half_width == 32):
    s_box_size = 8
  elif(half_width == 16):
    s_box_size = 4
  else:
    s_box_size = 16
  
  if(half_width == 32):
    #standard DES intial permutation table
    init_perm = [ 58, 50, 42, 34, 26, 18, 10, 2, 
                  60, 52, 44, 36, 28, 20, 12, 4, 
                  62, 54, 46, 38, 30, 22, 14, 6, 
                  64, 56, 48, 40, 32, 24, 16, 8, 
                  57, 49, 41, 33, 25, 17, 9, 1, 
                  59, 51, 43, 35, 27, 19, 11, 3, 
                  61, 53, 45, 37, 29, 21, 13, 5, 
                  63, 55, 47, 39, 31, 23, 15, 7 ]
    #standard DES expansion table
    exp = [ 32, 1, 2, 3, 4, 5,
                4, 5, 6, 7, 8, 9, 
                8, 9, 10, 11, 12, 13, 
                12, 13, 14, 15, 16, 17, 
                16, 17, 18, 19, 20, 21, 
                20, 21, 22, 23, 24, 25,
                24, 25, 26, 27, 28, 29,
                28, 29, 30, 31, 32, 1 ]
    #standard DES permutation table
    perm = [ 16, 7, 20, 21, 
                    29, 12, 28, 17, 
                    1, 15, 23, 26, 
                    5, 18, 31, 10, 
                    2, 8, 24, 14, 
                    32, 27, 3, 9, 
                    19, 13, 30, 6, 
                    22, 11, 4, 25 ]
    #standard DES inverse permutation table
    inv_init_perm = [ 40, 8, 48, 16, 56, 24, 64, 32, 
                39, 7, 47, 15, 55, 23, 63, 31, 
                38, 6, 46, 14, 54, 22, 62, 30, 
                37, 5, 45, 13, 53, 21, 61, 29, 
                36, 4, 44, 12, 52, 20, 60, 28, 
                35, 3, 43, 11, 51, 19, 59, 27, 
                34, 2, 42, 10, 50, 18, 58, 26, 
                33, 1, 41, 9, 49, 17, 57, 25 ]
  else:
    # to generate initial permutation table,expansion table,permutation table,inverse initial permutation table
    init_perm = [x for x in range(1,2*half_width+1)]
    seed(99)
    shuffle(init_perm)
    
    # to generate expansion table
    exp = [x for x in range(1,half_width+1)]
    pos = sample(range(1,half_width+1),len(roundk_bin[0]) - half_width)
    for i in pos:
      exp.append(i)
    seed(99)
    shuffle(exp)
    
    # to generate permutation table
    perm = [x for x in range(1,half_width+1)]
    seed(99)
    shuffle(perm)
    
    # to generate inverse initial permutation table
    inv_init_perm = [0 for i in range(len(init_perm))]
    for i,x in enumerate(init_perm):
      inv_init_perm[x-1] = i+1

  final = ""
  round_ciphertexts = []
  
  for plaintext in pt_blocks:
    plaintext = apply_permutation(plaintext, init_perm, len(init_perm))

  for plaintext in pt_blocks:
    left = plaintext[0:half_width]
    right = plaintext[half_width:]
    rct = []
    for i in range(rounds): 
      right_expanded = apply_permutation(right, exp, len(exp)) 
      x = calculatexor(roundk_bin[i], right_expanded)
      
      temp = ""
      for i in range(s_box_size):
          part = x[i*6:(i+1)*6]
          row = part[0] + part[5]
          row = int(row,2)
          col = part[1:-1]
          col = int(col,2)
          # mod 8 because of using same S-boxes circularly for a 64 bit half_width
          val = s_box[i%8][row][col] 
          temp += bin(val)[2:].zfill(4)
      
      
      temp = apply_permutation(temp, perm, len(perm)) 
      x = calculatexor(temp, left)
      left = x
      
      # Swaping at the end of each round
      left, right = right, left
      
      rct.append(str(left+right))

    round_ciphertexts.append(rct)
    #for final round
    left,right = right, left

  return (roundk_bin,round_ciphertexts)




def fun(plaintext: str,key: str, rounds: int=16, half_width:int=32, bp:int=0, bk:int=0):
  roundk_bin,round_ciphertexts   = desalgo(plaintext,key,rounds,half_width,0,0)
  roundk_bin1,round_ciphertexts1 = desalgo(plaintext,key,rounds,half_width,bp,bk)

  #we are printing the round keys to check how weak a given key is
  for i in range(len(roundk_bin)):
    print("Round key "+str(i)+":",roundk_bin[i])


  x_axis = [i for i in range(1,rounds+1)]
  y_axis=calc_diff(round_ciphertexts,round_ciphertexts1)

  #matplotlib library helps us to plot the graphs
  plt.plot(x_axis, y_axis)
  
  plt.xlabel('Round Number')
  plt.ylabel('Number of bits changed')
  plt.title('Avalanche effect Plot')
  
  plt.show()



"""Below is the code for designing user interface"""

root=Tk()

canvas=Canvas(root,width=700,height=300)
canvas.pack()

lab1=Label(root,text="Practical Assignment-1",fg="black",font=('Arial',18))
lab1.place(relx=0.25,rely=0,relheight=0.2,relwidth=0.5)

l1=Label(root,text="Plaintext",fg="black",font=('Verdana',11))
l1.place(relx=0,rely=0.16,relheight=0.1,relwidth=0.5)

l2=Label(root,text="Key",fg="black",font=('Verdana',11))
l2.place(relx=0.5,rely=0.16,relheight=0.1,relwidth=0.5)

#plaintext box
e1=Entry(root,fg="red",bg="yellow",border=5,font=('Arial',16))
e1.place(relx=0.02,rely=0.25,relheight=0.1,relwidth=0.4)

#ciphertext box
e2=Entry(root,fg="blue",bg="yellow",border=5,font=('Arial',16))
e2.place(relx=0.58,rely=0.25,relheight=0.1,relwidth=0.4)

l3=Label(root,text="Rounds",fg="black",font=('Verdana',11))
l3.place(relx=0,rely=0.36,relheight=0.1,relwidth=0.5)

l4=Label(root,text="Half Width",fg="black",font=('Verdana',11))
l4.place(relx=0.5,rely=0.36,relheight=0.1,relwidth=0.5)

#Rounds box
e3=Entry(root,fg="red",bg="yellow",border=5,font=('Arial',16))
e3.place(relx=0.02,rely=0.47,relheight=0.1,relwidth=0.4)

#Halfwidth box
e4=Entry(root,fg="blue",bg="yellow",border=5,font=('Arial',16))
e4.place(relx=0.58,rely=0.47,relheight=0.1,relwidth=0.4)

l5=Label(root,text="Change in bits in plaintext",fg="black",font=('Verdana',11))
l5.place(relx=0,rely=0.57,relheight=0.1,relwidth=0.5)

l6=Label(root,text="Change in bits in key",fg="black",font=('Verdana',11))
l6.place(relx=0.5,rely=0.57,relheight=0.1,relwidth=0.5)

#Change in bits in plaintext box
e5=Entry(root,fg="red",bg="yellow",border=5,font=('Arial',16))
e5.place(relx=0.02,rely=0.68,relheight=0.1,relwidth=0.4)

#Change in bits in key box
e6=Entry(root,fg="blue",bg="yellow",border=5,font=('Arial',16))
e6.place(relx=0.58,rely=0.68,relheight=0.1,relwidth=0.4)


#button to encipher the plaintext to ciphertext
but1=Button(root,text="ENCRYPT",command=lambda : fun(e1.get(),e2.get(),int(e3.get()),int(e4.get()),int(e5.get()),int(e6.get())),bg="green")
but1.place(relx=0.35,rely=0.9,relheight=0.07,relwidth=0.3)


root.mainloop()

