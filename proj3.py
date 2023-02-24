PAGE_SIZE = 256
PHYS_MEM_SIZE = 256
def extractedbits(no,k,pos): 
    bi = bin(no)
    bi=bi[2:]
    pos=pos-1
    while(len(bi) !=32):
        bi="0"+bi
    s=bi[31-pos-k:31-pos]
    return int(s,2)


def main():
    PAGE_SIZE = 256
    adds=[]
    TLB=[]
    ptable=[]
    physicalMem=[None]*PHYS_MEM_SIZE
    tlbIndex=0
    rows, cols=16,2
    hit=0
    openFrame=0
    totalfaults=0
    totalhits=0

    for i in range(rows):
        col = []
        for j in range(cols):
            col.append(-1)
        TLB.append(col)
    
    for i in range(256):
        ptable.append(-1)

        
    with open('./Program_3/addresses.txt') as addresses:
        for line in addresses:
            adds.append(int(line))
    for i in adds:
        pagenum=extractedbits(i,8,8)
        offset=extractedbits(i,8,0)
        framenumber=None
        hit=0
        for j in range(rows):
            if(TLB[j][0]==pagenum):
                hit=1
                totalhits+=1
                framenumber=tlb[j][1]
                break


    

        if(not hit):
            if(ptable[pagenum]==-1):
                with open("./Program_3/BACKING_STORE.bin", mode='rb') as file:
                    file.seek(pagenum*256)
                    b=file.read(256)
                    physicalMem[openFrame]=b.hex()
                    openFrame+=1
                ptable[pagenum] = openFrame-1
                totalfaults+=1
            framenumber=ptable[pagenum]
            TLB[tlbIndex][0]=pagenum
            TLB[tlbIndex][1]=framenumber
            tlbIndex=(tlbIndex+1)%rows
        index=(framenumber)
        hexa = physicalMem[index]
        value=hexa[offset*2:(offset*2)+2]
        x=int(value,16)
        
        print(i,offset,value,x,index,hexa,'\n')








if __name__ == "__main__":
    main()