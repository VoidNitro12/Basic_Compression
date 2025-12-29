import json
class Encode():
    def __init__(self):
        self.prob_list = []
        self.char_list = []
        self.nodes = []
        self.codes = {}
        self.rev_codes = []
        self.encoded = []  
        self.decoded = []
        self.decoded_text = ""  
    
    def Sort(self,text):
        self.text = text
        total = len(self.text)
        for char in self.text:
            if char not in self.char_list:   
                num_times = self.text.count(char)
                prob = (num_times/total) * 100

                if self.char_list == []: 
                    self.prob_list.append(prob)
                    self.char_list.append(char)
                else: 
                    for i in range(len(self.prob_list) ):
                        if prob > self.prob_list[i]:
                            self.prob_list.insert(i,prob)
                            self.char_list.insert(i,char)
                            break
                        else:
                            self.prob_list.append(prob)
                            self.char_list.append(char)
                            break
    
    def Tree(self):
        for char, prob in zip(self.char_list, self.prob_list):
            self.nodes.append(Node(char, prob,True))

        sorted_list = self.nodes.copy()
        uid = 0
        while len(sorted_list)> 1:
            current = sorted_list[0]
            next = sorted_list[1]

            total = current.weight + next.weight
            sorted_list.append(Node(uid,total,False))
            sorted_list[-1].left = current
            sorted_list[-1].right = next

            sorted_list.pop(0)
            sorted_list.pop(0)

            sorted_list.sort(key=lambda n: n.weight)
            uid +=1
        self.nodes = sorted_list

    def Assign_codes(self,node,code=""):
        if node.leaf_node == False :
            code + "0"
            if node.left != None and node.right != None:
                self.Assign_codes(node.left,code + "0")
                self.Assign_codes(node.right, code + "1")
        elif node.leaf_node:
            self.codes[node.obj] = code
            self.rev_codes = {v: k for k,v in self.codes.items()}

    def Final(self):
        for char in self.text:
            self.encoded.append(self.codes[char])

    def Decode(self):
        for obj in self.encoded:
            self.decoded.append(self.rev_codes[obj])
        self.decoded_text ="".join(self.decoded)

    def Test(self,text):
        print(f"For text : {text}")
        self.Sort(text)
        self.Tree()
        self.Assign_codes(self.nodes[0])
        self.Final()
        self.Decode()
        print(f"Encoded text : {self.encoded}")
        print(f"Decoded text : {self.decoded}")
        print(f"Result : {self.decoded_text}")

    def encode_txt(self):
        try:
            with open("/home/esmond/Desktop/Compression check/Test.txt","r") as file:
                info = file.read()
        except FileNotFoundError:
            with open("/home/esmond/Desktop/Compression check/Test.txt","w") as file:
                file.write("Made TXT file")

            with open("/home/esmond/Desktop/Compression check/Test.txt","r") as file:
                info = file.read()

        self.Sort(info)
        self.Tree()
        self.Assign_codes(self.nodes[0])
        self.Final()

        encode_bit_string = self.encoded #"".join(self.encoded)

        with open("/home/esmond/Desktop/Compression check/Test_encoded.json","w") as file:
                json.dump(encode_bit_string,file,indent=4)

        with open("/home/esmond/Desktop/Compression check/Test_encoded_Refcode.json","w") as file:
                json.dump(self.rev_codes,file,indent=4)

    def decode_txt(self):
        with open("/home/esmond/Desktop/Compression check/Test_encoded.json","r") as file:
            info = json.load(file)
        
        with open("/home/esmond/Desktop/Compression check/Test_encoded_Refcode.json","r") as file:
            refcode = json.load(file)
        
        decoded = []
        
        for obj in info:
            decoded.append(refcode[obj])
        decoded_text ="".join(decoded)

        with open("/home/esmond/Desktop/Compression check/Test_decoded.txt","w") as file:
                file.write(decoded_text) 

class Node:
    def __init__(self, char, prob,leaf):
        self.obj = char
        self.weight = prob
        self.left = None
        self.right = None
        self.leaf_node = leaf

    def __repr__(self):
        left_str = f"Node('{self.left.obj}', {self.left.weight})" if self.left else "None"
        right_str = f"Node('{self.right.obj}', {self.right.weight})" if self.right else "None"
        return f"Node('{self.obj}', {self.weight}, Leaf_Node={self.leaf_node}, code = {self.code} left={left_str}, right={right_str})"

text = "Loveday check this out"
Test = Encode()
Test.decode_txt()
