import os
import tkinter as tk

# installs the requests library
batList = []
print('Searching for "requestsInstaller.bat" this might take a while')

for root, dirs, files in os.walk('C:\\'):
    if "requestsInstaller.bat" in files:
        path = os.path.join(root, "requestsInstaller.bat")
        batList.append(path)

print("Installing the requests library")
print(" ")
os.system(r'{}'.format(batList[0]))

# asks the user if they want to open the api thingy or not
root = tk.Tk()

root.configure(background="white")
root.maxsize(200, 90)
root.geometry("200x90")

def Yes():
    os.system("python3 {}".format(batList[0].replace("requestsInstaller.bat", "WAS.py")))
    root.destroy()
def No():
    root.destroy()
    
text = tk.Label(root, text="Do you want to open the api thingy?")
text.pack()
button = tk.Button(root, text="Yes", command=Yes)
button.pack()
button2 = tk.Button(root, text="No", command=No)
button2.place(x=86, y=50)

root.mainloop()