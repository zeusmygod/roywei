def CreatePyramid():
    file1=open('A1-111502016/input.txt','r')
    file2=open('A1-111502016/output.txt','w')
    number=int(file1.read())
    base=number*2-1
    for i in range(1,base,2):
        space=number-((i+1)//2)
        file2.write(" "*space +"*"*i+"\n")    
    file2.write("*"*base)
    file1.close()
    file2.close()
CreatePyramid()