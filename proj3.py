import struct
PAGE_SIZE = 256
PHYS_MEM_SIZE = 3

# first in first out
def fifo(physicalMem,b,openFrame,rows,ptable,pagenum,TLB):
    
    physicalMem[openFrame[0]]=b.hex()
    for i in range(16):
        if(TLB[i][1]==openFrame[0]):
            TLB[i][0]=pagenum
    ptable[pagenum]=openFrame[0]
    for i in range(len(ptable)):
        if(ptable[i]==openFrame[0] and i!=pagenum):
            ptable[i]=-1
    openFrame[0]=(openFrame[0]+1)%PHYS_MEM_SIZE

# least recently used
def lru(physicalMem,b,rows,ptable,pagenum,TLB,stack):
    index=0
    try:
        index=physicalMem.index(None)
    except:   
        index=stack.data
    
    print("LRUFrame",index)
    physicalMem[index]=b.hex()
    
    for i in range(16):
        if(TLB[i][1]==index):
            TLB[i][0]=pagenum
    ptable[pagenum]=index
    for i in range(len(ptable)):
        if(ptable[i]==index and i!=pagenum):
            ptable[i]=-1
def opt(physicalMem,b,rows,ptable,pagenum,TLB,optmap,optstack):
    index=0
    m=-1
    try:
        index=physicalMem.index(None)
    except:   
        
        for i in range(len(optstack)):
            print(optstack)
            if len(optmap[optstack[i]]) ==0:
                m=optstack[i]
                break
            if(optmap[optstack[i]][0]>m):
                m=optstack[i]

        index=ptable[m]
        optstack.remove(m)
#17 1 54 
    
    optstack.append(pagenum)  
    physicalMem[index]=b.hex()
    for i in range(16):
        if(TLB[i][1]==index):
            TLB[i][0]=pagenum
    ptable[pagenum]=index
    for i in range(len(ptable)):
        if(ptable[i]==index and i!=pagenum):
            ptable[i]=-1


def extractedbits(no,k,pos): 
    bi = bin(no)
    bi=bi[2:]
    pos=pos-1
    while(len(bi) !=32):
        bi="0"+bi
    s=bi[31-pos-k:31-pos]
    return int(s,2)

# find node in list by value, return None if not found
def findNode(head, data):
    #if not isinstance(head, Node):
     #       raise TypeError("findNode 'head' must be a Node")
    node = head
    while(node != None):
        if(node.data == data):
            return node
        node = node.next
    return None

# print current state of list
def printLRU(head):
    node = head
    while(node != None):
        print(node.data,"\n")
        node = node.next



class Node:
   def __init__(self, data=None):
      self.data = data
      self.next = None
      self.prev = None


def main():
    PAGE_SIZE = 256
    lruhead= None
    lrutail= None
    optmap={}
    optstack=[]
    adds=[]
    TLB=[]
    ptable=[]
    physicalMem=[None]*PHYS_MEM_SIZE
    tlbIndex=0
    rows, cols=16,2
    hit=0
    openFrame=[0]
    totalfaults=0
    totalhits=0

    for i in range(rows):
        col = []
        for j in range(cols):
            col.append(-1)
        TLB.append(col)
    
    for i in range(256):
        ptable.append(-1)

        
    with open('./Program_3/one.txt') as addresses:
        for idx,line in enumerate(addresses):
            x = int(line)
            adds.append(int(line))
            print(x%256)
            if extractedbits(x,8,8) in optmap.keys():
                optmap[extractedbits(x,8,8)].append(idx)
            else:
                optmap[extractedbits(x,8,8)]=[]
    for i in adds:
        print(optmap.keys())
        if len(optmap[extractedbits(x,8,8)])!=0:
            optmap[extractedbits(x,8,8)].pop(0)
        pagenum=extractedbits(i,8,8)
        offset=extractedbits(i,8,0)
        framenumber=None
        hit=0
        for j in range(rows):
            if(TLB[j][0]==pagenum):
                hit=1
                totalhits+=1
                framenumber=TLB[j][1]
                break


    

        if(not hit):
            print("TLB MISS")
            if(ptable[pagenum]==-1):
                with open("./Program_3/BACKING_STORE.bin", mode='rb') as file:
                    file.seek(pagenum*256)
                    b=file.read(256)
                    # lru(physicalMem,b,rows,ptable,pagenum,TLB,lrutail)
                    opt(physicalMem,b,rows,ptable,pagenum,TLB,optmap,optstack)
                    print("PAGEFAULT")
                totalfaults+=1
            framenumber=ptable[pagenum]
            TLB[tlbIndex][0]=pagenum
            TLB[tlbIndex][1]=framenumber
            tlbIndex=(tlbIndex+1)%rows
        index=(framenumber)
        hexa = physicalMem[index]
        n = findNode(lruhead,index)
        print(index,n)
        if(n):
            print(n.data)
            # if node at beginning of list, do nothing
            if(lruhead.data!=n.data):
                # middle of list
                if(n.next!= None and n.prev!=None):
                    n.prev.next=n.next
                    n.next.prev=n.prev
                    n.prev = None
                    n.next = lruhead
                    lruhead.prev = n
                    lruhead = n
                # end of list
                else:
                    # update tail
                    lrutail = n.prev
                    n.prev.next=None
                    n.prev = None
                    n.next = lruhead
                    lruhead.prev = n
                    lruhead = n
        else:
            # if index not in list, add it
            nod=Node()
            nod.data=index
            # if empty list
            if (lruhead==None):
                nod.prev=None
                nod.next=None
                lrutail=nod
                lruhead=nod
            # not empty
            else:
                nod.prev=None
                nod.next=lruhead
                lruhead.prev=nod
                lruhead=nod
        printLRU(lruhead)
        value=hexa[offset*2:(offset*2)+2]
        bits = bin(int(value, 16))[2:].zfill(8)

        if bits[0] == "1":
            signed_value = -((int("".join("1" if bit == "0" else "0" for bit in bits), 2) + 1) & 0xff)
        else:
            signed_value = int(bits, 2)

        print(i,pagenum,signed_value,index,hexa,'\n')
    print("Number of Translated Addresses = ",len(adds))
    print("Page Faults = ",totalfaults)
    print("Page Fault Rate = ", totalfaults/len(adds))
    print("TLB Hits = ", totalhits)
    print("TLB Misses = ",(len(adds))-totalhits)
    print("TLB Hit Rate = ", totalhits/len(adds))
    print("size of physmem",PHYS_MEM_SIZE)







if __name__ == "__main__":
    main()