chain = coc = '"A8zx","7r:ti","2","test","test2"'

sep = ',' 
esp = coc.count(sep)

if esp > 4:
    print("Veuillez ne rentrer que 5 recherches max.")
else :
    startR = 0
    total = 0
    if coc.count(sep)!=0:
        endR = coc.index(sep)
    else:
        endR = len(coc)
        
    listR = []
    pos=endR

    for i in range(0,esp):
        if i ==0 : total = total + pos
        elif i==1 : total = total + pos + i
        elif i==2 : total = total + pos + i
        elif i==3 : total = total + pos + i+(2-i)
        
        listR.append(total)
        coc = coc[endR+1:]
        if coc.count(sep)!=0:
            endR = coc.index(sep)+1
            pos = coc.index(sep)
        else : break    
    
    for j in range(len(listR)):
        print(listR[j])