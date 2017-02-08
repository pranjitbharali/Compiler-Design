class node:
    count=0;
    def __init__(self, typ):
        self.typ=typ

def print_tree(root,values):
    if(hasattr(root,'left')):
        print_tree(root.left,values)
    if(hasattr(root,'down')):
        print_tree(root.down,values)
    print("type =  ",root.typ,"\t\talphabet : ",values[root.index],"\t\t nullable : ",root.nullable,"\t\t firstpos : ",root.firstpos,"\t\t lastpos : ",root.lastpos)
    if(hasattr(root,'right')):
        print_tree(root.right,values)
    return

def infix2postfix(S):
    stack = [];
    new=""
    for c in S:
        if(c=='*' or c=='('):
            stack.append(c)
        elif(c=='.'):
            while(len(stack)>0 and (stack[-1]=='.' or stack[-1]=='*')):
                new+=stack.pop()
            stack.append(c)
        elif(c=='|'):
            while(len(stack)>0 and (stack[-1]=='.' or stack[-1]=='*' or stack[-1]=='|' ) ):
                new+=stack.pop()
            stack.append(c)
        elif(c==')'):
            while(len(stack)>0 and stack[-1]!='('):
                new+=stack.pop()
            stack.pop()
        else:
            new+=str(c)
    while(len(stack)>0):
        new+=stack.pop()
    return new

def processing(S):
    types = {'.':"cat", '|':"or", '*':"star" }
    values = {'null' : "null"}
    followpos={}
    stack = [];
    root = node("root")
    print('in-order traversal of the tree : ')
    for c in S:
        if(c=='.' or c=='|'):
            b=stack.pop()
            a=stack.pop()
            new = node(types[c])
            if(c=='.'):
                new.nullable = a.nullable and b.nullable
                if(a.nullable):
                    new.firstpos = a.firstpos|b.firstpos
                else:
                    new.firstpos = a.firstpos
                if(b.nullable):
                    new.lastpos = a.lastpos|b.lastpos
                else:
                    new.lastpos = b.lastpos
                for i in a.lastpos:
                	if(i in followpos):
                		followpos[i]=followpos[i]|b.firstpos
                	else:
                		followpos[i]=b.firstpos
            else:
                new.nullable = a.nullable or b.nullable
                new.firstpos = a.firstpos|b.firstpos
                new.lastpos = a.lastpos|b.lastpos
            new.index = 'null'
            new.left=a
            new.right=b
            stack.append(new)
        elif(c=='*'):
            a=stack.pop()
            for i in a.lastpos:
                	if(i in followpos):
                		followpos[i]=followpos[i]|a.firstpos
                	else:
                		followpos[i]=a.firstpos
            new = node(types[c])
            new.down = a
            new.nullable = True
            new.firstpos=a.firstpos
            new.lastpos=a.lastpos
            new.index = 'null'
            stack.append(new)
        elif(c=='#'):
            node.count+=1
            values[node.count]='#'
            a=stack.pop()
            b=node("finish")
            b.index=node.count
            b.nullable = False
            b.firstpos=set([node.count])
            b.lastpos=set([node.count])
            root.left=a
            root.right=b
            root.index='null'
            root.nullable = False
            if(a.nullable):
                root.firstpos = a.firstpos|b.firstpos
            else:
                root.firstpos = a.firstpos
            root.lastpos = b.lastpos
            for i in a.lastpos:
                	if(i in followpos):
                		followpos[i]=followpos[i]|b.firstpos
                	else:
                		followpos[i]=b.firstpos
        else:
            node.count+=1
            values[node.count]=c
            new=node("alphabet")
            new.index=node.count
            new.nullable = False
            new.firstpos = set([node.count])
            new.lastpos = set([node.count])
            stack.append(new)
    print_tree(root,values)
    print("Total leaf nodes : ",node.count)
    print("followpos :",followpos)
    return

S=input("Enter infix regular expression (operators are '.' or '|' or '*' or '(' or ')' ) :  ")
new=infix2postfix(S)
new=new+'#'
print(new)
processing(new)
