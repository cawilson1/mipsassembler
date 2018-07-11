#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def main():
    
    with open(('assembly_program.asm'), "r") as f:
            assemblyCode = f.read()
    f.closed
    print(assemblyCode)
    assemblyCodeSplitByLine = assemblyCode.split("\n")
    
    #whenever read from a file, split method above always creates newlines
    del assemblyCodeSplitByLine[-1]
    
    assembleInstructions(assemblyCodeSplitByLine)
    
#run through file twice, first time for labels, second time for rest
def assembleInstructions(assemblyCode):
    
    firstPassThrough = True
    currentLine = 0
    
    i = 0
    while(i < 2):
        for line in assemblyCode:
            if not line.strip() == '':#ignore blank lines
                instruction = line.split(" ")
                if(checkOperation(instruction, firstPassThrough, currentLine)):#if false is returned, the line consists only of a label
                    currentLine += 1
        i += 1
        firstPassThrough = False
        currentLine = 0
    
def checkOperation(instruction, firstPassThrough, currentLine):
    
    isInstructionLine = True #return value. true by default. If the line contains only a label, it is change to false
    
    if not firstPassThrough and ':' in instruction[0] and len(instruction) > 1 and not instruction[1] == '': #and not instruction[0][-1] == ':':
       #this line contains a label and an instruction. ignore label and go to instruction
       print(instruction[0],' before')
       if(instruction[0][-1]==':'):#The label has a space between it and the instruction
           instruction = removeLabelFromLine(instruction)
       else:
           instruction = splitLabelFromInstruction(instruction)
       print(instruction[0],' after')
      
    
    if instruction[0] == 'add':
        if not firstPassThrough:
            binaryInstruction = add(instruction)
    elif instruction[0] == 'sub':
        if not firstPassThrough:
            binaryInstruction = sub(instruction)
    elif instruction[0] == 'addi':
        if not firstPassThrough:
            binaryInstruction = addi(instruction)
    elif instruction[0] == 'and':
        if not firstPassThrough:
            binaryInstruction = andFunc(instruction)
    elif instruction[0] == 'or':
        if not firstPassThrough:
            binaryInstruction = orFunc(instruction)
    elif instruction[0] == 'xor':
        if not firstPassThrough:
            binaryInstruction = xor(instruction)
    elif instruction[0] == 'nor':
        if not firstPassThrough:
            binaryInstruction = nor(instruction)
    elif instruction[0] == 'beq':
        if not firstPassThrough:
            binaryInstruction = beq(instruction, currentLine)#needs to know current line
    elif instruction[0] == 'bne':
        if not firstPassThrough:
            binaryInstruction = bne(instruction, currentLine)#needs to know current line
    elif instruction[0] == 'j':
        if not firstPassThrough:
            binaryInstruction = j(instruction)
    elif instruction[0] == 'jal':
        if not firstPassThrough:
            binaryInstruction = jal(instruction)
    elif instruction[0] == 'sll':
        if not firstPassThrough:
            binaryInstruction = sll(instruction)
    elif instruction[0] == 'srl':
        if not firstPassThrough:
            binaryInstruction = srl(instruction)
    elif instruction[0] == 'lw':
        if not firstPassThrough:
            binaryInstruction = lw(instruction)
    elif instruction[0] == 'lb':
        if not firstPassThrough:
            binaryInstruction = lb(instruction)
    elif instruction[0] == 'lh':
        if not firstPassThrough:
            binaryInstruction = lh(instruction)
    elif instruction[0] == 'sw':
        if not firstPassThrough:
            binaryInstruction = sw(instruction)
    elif instruction[0] == 'sb':
        if not firstPassThrough:
            binaryInstruction = sb(instruction)
    elif instruction[0] == 'sh':
        if not firstPassThrough:
            binaryInstruction = sh(instruction)
    elif instruction[0] == 'syscall':
        if not firstPassThrough:
            binaryInstruction = syscall(instruction)
    elif instruction[0] == 'slti':
        if not firstPassThrough:
            binaryInstruction = slti(instruction)
    elif instruction[0] == 'andi':
        if not firstPassThrough:
            binaryInstruction = andi(instruction)
    elif instruction[0] == 'ori':
        if not firstPassThrough:
            binaryInstruction = ori(instruction)
    elif instruction[0] == 'xori':
        if not firstPassThrough:
            binaryInstruction = xori(instruction)
    elif instruction[0] == 'lui':
        if not firstPassThrough:
            binaryInstruction = lui(instruction)
    elif instruction[0] == 'jr':
        if not firstPassThrough:
            binaryInstruction = jr(instruction)
    elif instruction[0] == 'mult':
        if not firstPassThrough:
            binaryInstruction = mult(instruction)
    elif instruction[0] == 'div':
        if not firstPassThrough:
            binaryInstruction = div(instruction)
    
    else:
        if firstPassThrough:
            print("first pass through")
            key = instruction[0]
            
            #proper syntax for a label
            if key.endswith(':') and len(key)>1:
                Labels[key[:-1]] = currentLine#remove the colon
                
                if(not len(instruction) > 1 or not key == ''):
                    print(key, ' does not increment curent line')
                    isInstructionLine = False
        else:
            if not instruction[0][:-1] in Labels:
                binaryInstruction = instruction[0] + " is not a valid operation. If using a label, make sure it ends with a colon."
            else:
                binaryInstruction = ''#ignore current line, it is a label. set binary instruction to print nothing
        
    #second part of and statement prevents printing of unecessary line
    if not firstPassThrough and not binaryInstruction == '':
        print(binaryInstruction)
    return isInstructionLine

#the value at the first index is a label. Remove it and return the instruction
def removeLabelFromLine(instruction):
    newList = []
    for item in instruction[1:]:
        newList.append(item)
        
    return newList

def splitLabelFromInstruction(instruction):
    newList = []
    temp = instruction[0]
    tempList = temp.split(':')
    print('the split:::: ',tempList[1])
    newList.append(tempList[0])
    newList.append(tempList[1])
    for item in instruction[1:]:
        newList.append(item)
        
    return newList

#functions to handle individual instructions
def add(instruction):
    #wrong format for add instruction
    if(len(instruction)!=4):
        print("incorrect format for add instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('000000')
        
        #find and append register values
        regList = getRTypeRegisters(instruction)
        
        for reg in regList:
            binaryInstructionList.append(reg)

        #shamt
        binaryInstructionList.append('00000')
        #funct
        binaryInstructionList.append('100000')
        binaryInstruction = ''.join(binaryInstructionList)
    
    return binaryInstruction
    
    
def sub(instruction):
    #wrong format for sub instruction
    if(len(instruction)!=4):
        print("incorrect format for sub instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('000000')
        
        #find and append register values
        regList = getRTypeRegisters(instruction)
        
        for reg in regList:
            binaryInstructionList.append(reg)
            
        #shamt
        binaryInstructionList.append('00000')
        #funct
        binaryInstructionList.append('100010')
        binaryInstruction = ''.join(binaryInstructionList)
    
    return binaryInstruction
    
def andFunc(instruction):
    #wrong format for and instruction
    if(len(instruction)!=4):
        print("incorrect format for and instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('000000')
        
        #find and append register values
        regList = getRTypeRegisters(instruction)
        
        for reg in regList:
            binaryInstructionList.append(reg)
            
        #shamt
        binaryInstructionList.append('00000')
        #funct
        binaryInstructionList.append('100100')
        binaryInstruction = ''.join(binaryInstructionList)
    
    return binaryInstruction

def orFunc(instruction):
    #wrong format for or instruction
    if(len(instruction)!=4):
        print("incorrect format for or instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('000000')
        
        #find and append register values
        regList = getRTypeRegisters(instruction)
        
        for reg in regList:
            binaryInstructionList.append(reg)
            
        #shamt
        binaryInstructionList.append('00000')
        #funct
        binaryInstructionList.append('100101')
        binaryInstruction = ''.join(binaryInstructionList)
    
    return binaryInstruction
    
def xor(instruction):
    #wrong format for xor instruction
    if(len(instruction)!=4):
        print("incorrect format for xor instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('000000')
        
        #find and append register values
        regList = getRTypeRegisters(instruction)
        
        for reg in regList:
            binaryInstructionList.append(reg)
            
        #shamt
        binaryInstructionList.append('00000')
        #funct
        binaryInstructionList.append('100110')
        binaryInstruction = ''.join(binaryInstructionList)
    
    return binaryInstruction
    
def nor(instruction):
    #wrong format for nor instruction
    if(len(instruction)!=4):
        print("incorrect format for nor instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('000000')
        
        #find and append register values
        regList = getRTypeRegisters(instruction)
        
        for reg in regList:
            binaryInstructionList.append(reg)
            
        #shamt
        binaryInstructionList.append('00000')
        #funct
        binaryInstructionList.append('100111')
        binaryInstruction = ''.join(binaryInstructionList)
    
    return binaryInstruction

def slt(instruction):
    #wrong format for slt instruction
    if(len(instruction)!=4):
        print("incorrect format for slt instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('000000')
        
        #find and append register values
        regList = getRTypeRegisters(instruction)
        
        for reg in regList:
            binaryInstructionList.append(reg)
            
        #shamt
        binaryInstructionList.append('00000')
        #funct
        binaryInstructionList.append('101010')
        binaryInstruction = ''.join(binaryInstructionList)
    
    return binaryInstruction
    

def sll(instruction):
    if(len(instruction)!=4):
        print("incorrect format for sll instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode and $rd
        binaryInstructionList.append('00000000000')
        valuesList = getShiftInstructionValues(instruction)
        
        #rs, rt and shamt
        for value in valuesList:
            binaryInstructionList.append(value)
            
        #funct
        binaryInstructionList.append('000000')
        binaryInstruction = ''.join(binaryInstructionList)
        
    return binaryInstruction

def srl(instruction):
    if(len(instruction)!=4):
        print("incorrect format for sll instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode and $rd
        binaryInstructionList.append('00000000000')
        valuesList = getShiftInstructionValues(instruction)
        
        #rs, rt and shamt
        for value in valuesList:
            binaryInstructionList.append(value)
            
        #funct
        binaryInstructionList.append('000010')
        binaryInstruction = ''.join(binaryInstructionList)
        
    return binaryInstruction
        

def addi(instruction):
    #wrong format for addi instruction
    if(len(instruction)!=4):
        print("incorrect format for addi instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('001000')
        
        regList = getITypeRegisters(instruction, False)
        for reg in regList:
            binaryInstructionList.append(reg)

        binaryInstruction = ''.join(binaryInstructionList)
    
    return binaryInstruction


def beq(instruction, currentLine):
    #wrong format for beq instruction
    if(len(instruction)!=4):
        print("incorrect format for beq instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('000100')
        
        regList = getITypeRegisters(instruction, True)
        for reg in regList:
            binaryInstructionList.append(reg)

        binaryInstructionList.append(findBranchLabelAddress(instruction[3], currentLine))
        
        binaryInstruction = ''.join(binaryInstructionList)
    
    return binaryInstruction


def bne(instruction, currentLine):
    #wrong format for bne instruction
    if(len(instruction)!=4):
        print("incorrect format for bne instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('000101')
        
        regList = getITypeRegisters(instruction, True)
        for reg in regList:
            binaryInstructionList.append(reg)
        
        binaryInstructionList.append(findBranchLabelAddress(instruction[3], currentLine))

        binaryInstruction = ''.join(binaryInstructionList)
    
    return binaryInstruction

def j(instruction):
    if(len(instruction)!=2):
        print("incorrect format for j instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('000010')
        binaryInstructionList.append(findJLabelAddress(instruction[1]))
        binaryInstruction = ''.join(binaryInstructionList)
        
    return binaryInstruction

def jal(instruction):
    if(len(instruction)!=2):
        print("incorrect format for j instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('000011')
        binaryInstructionList.append(findJLabelAddress(instruction[1]))
        binaryInstruction = ''.join(binaryInstructionList)
        
    return binaryInstruction

def checkForNegativeAddressJump(address):
    if(int(address) < 0):
        print("The instruction below requests a jump to a negative address")

def lw(instruction):
    if(len(instruction)!=3):
        print("incorrect format for lw instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('100011')
        
        valList = getLoadAndStoreRegisters(instruction)
        for val in valList:
            binaryInstructionList.append(val)
        
        binaryInstruction = ''.join(binaryInstructionList)
        
    return binaryInstruction

def lb(instruction):
    if(len(instruction)!=3):
        print("incorrect format for lb instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('100000')
        
        valList = getLoadAndStoreRegisters(instruction)
        for val in valList:
            binaryInstructionList.append(val)
        
        binaryInstruction = ''.join(binaryInstructionList)
        
    return binaryInstruction

def lh(instruction):
    if(len(instruction)!=3):
        print("incorrect format for lh instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('100001')
        
        valList = getLoadAndStoreRegisters(instruction)
        for val in valList:
            binaryInstructionList.append(val)
        
        binaryInstruction = ''.join(binaryInstructionList)
        
    return binaryInstruction

def sw(instruction):
    if(len(instruction)!=3):
        print("incorrect format for sw instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('101011')
        
        valList = getLoadAndStoreRegisters(instruction)
        for val in valList:
            binaryInstructionList.append(val)
        
        binaryInstruction = ''.join(binaryInstructionList)
        
    return binaryInstruction

def sb(instruction):
    if(len(instruction)!=3):
        print("incorrect format for sb instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('101000')
        
        valList = getLoadAndStoreRegisters(instruction)
        for val in valList:
            binaryInstructionList.append(val)
        
        binaryInstruction = ''.join(binaryInstructionList)
        
    return binaryInstruction

def sh(instruction):
    if(len(instruction)!=3):
        print("incorrect format for sh instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('101001')
        
        valList = getLoadAndStoreRegisters(instruction)
        for val in valList:
            binaryInstructionList.append(val)
        
        binaryInstruction = ''.join(binaryInstructionList)
        
    return binaryInstruction

def syscall(instruction):
    if(len(instruction)!=1):
        print("incorrect format for syscall")
        binaryInstruction = None
    else:
        binaryInstruction = '000000xxxxxxxxxxxxxxxxxxxx001100'
    return binaryInstruction

def slti(instruction):
    #wrong format for slti instruction
    if(len(instruction)!=4):
        print("incorrect format for slti instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('001010')
        
        regList = getITypeRegisters(instruction, False)
        for reg in regList:
            binaryInstructionList.append(reg)

        binaryInstruction = ''.join(binaryInstructionList)
    
    return binaryInstruction
    
def andi(instruction):
    #wrong format for andi instruction
    if(len(instruction)!=4):
        print("incorrect format for andi instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('001100')
        
        regList = getITypeRegisters(instruction, False)
        for reg in regList:
            binaryInstructionList.append(reg)

        binaryInstruction = ''.join(binaryInstructionList)
    
    return binaryInstruction

def ori(instruction):
    #wrong format for ori instruction
    if(len(instruction)!=4):
        print("incorrect format for ori instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('001101')
        
        regList = getITypeRegisters(instruction, False)
        for reg in regList:
            binaryInstructionList.append(reg)

        binaryInstruction = ''.join(binaryInstructionList)
    
    return binaryInstruction

def xori(instruction):
    #wrong format for xori instruction
    if(len(instruction)!=4):
        print("incorrect format for xori instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('001110')
        
        regList = getITypeRegisters(instruction, False)
        for reg in regList:
            binaryInstructionList.append(reg)

        binaryInstruction = ''.join(binaryInstructionList)
    
    return binaryInstruction

def lui(instruction):
    #wrong format for lui instruction
    if(len(instruction)!=3):
        print("incorrect format for lui instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('001111')
        #rs is 0
        binaryInstructionList.append('00000')
        #rt
        binaryInstructionList.append(getRegisterValue(instruction[1]))
        #shamt
        binaryInstructionList.append(getImmediateValue(instruction[2], 16))

        binaryInstruction = ''.join(binaryInstructionList)
    
    return binaryInstruction

def jr(instruction):
    #wrong format for jr instruction
    if(len(instruction)!=2):
        print("incorrect format for jr instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('000000')
        #register
        binaryInstructionList.append(getRegisterValue(instruction[1]))
        #rmaining values
        binaryInstructionList.append('000000000000000')
        #funct
        binaryInstructionList.append('001000')
        binaryInstruction = ''.join(binaryInstructionList)
    
    return binaryInstruction

def mult(instruction):
    #wrong format for mult instruction
    if(len(instruction)!=3):
        print("incorrect format for mult instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('000000')
        #rs
        binaryInstructionList.append(getRegisterValue(instruction[1]))
        #rt
        binaryInstructionList.append(getRegisterValue(instruction[2]))

        #other values
        binaryInstructionList.append('0000000000')
        #funct
        binaryInstructionList.append('011000')
        binaryInstruction = ''.join(binaryInstructionList)
    
    return binaryInstruction

def div(instruction):
    #wrong format for div instruction
    if(len(instruction)!=3):
        print("incorrect format for div instruction")
        binaryInstruction = None
    else:
        binaryInstructionList = []
        #opcode
        binaryInstructionList.append('000000')
        #rs
        binaryInstructionList.append(getRegisterValue(instruction[1]))
        #rt
        binaryInstructionList.append(getRegisterValue(instruction[2]))
        #other values
        binaryInstructionList.append('0000000000')
        #funct
        binaryInstructionList.append('011010')
        binaryInstruction = ''.join(binaryInstructionList)
    
    return binaryInstruction

def getRTypeRegisters(instruction):
    registersList = []
    #$rs
    registersList.append(getRegisterValue(instruction[2]))
    #$rt
    registersList.append(getRegisterValue(instruction[3]))
    #$rd
    registersList.append(getRegisterValue(instruction[1]))
    
    return registersList


def getITypeRegisters(instruction, branchInstruction):
    registersList = []
    #$rs
    registersList.append(getRegisterValue(instruction[2]))
    #$rt
    registersList.append(getRegisterValue(instruction[1]))
    if not branchInstruction:#branch has its own 3rd parameter value method
        #imm
        registersList.append(getImmediateValue(instruction[3], 16))
    
    return registersList

def getLoadAndStoreRegisters(instruction):
    registersList = []
    #returns immediate as parsedLoadInstruction[0] and register at parsedLoadInstruction[1]
    parsedLoadInstruction = parseLoadInstruction(instruction[2])
    #$rs
    registersList.append(getRegisterValue(parsedLoadInstruction[1]))
    #$rt
    registersList.append(getRegisterValue(instruction[1]))
    #imm
    registersList.append(getImmediateValue(parsedLoadInstruction[0], 16))
    
    return registersList


def parseLoadInstruction(instruction):
    instructionList = instruction.split("(")
    instructionList[1] = instructionList[1].replace(")", "")

    return instructionList
    
def getShiftInstructionValues(instruction):
    valuesList = []
    valuesList.append(getRegisterValue(instruction[2]))
    valuesList.append(getRegisterValue(instruction[1]))
    
    if(int(instruction[3])<0):
        print("negative shift amount requested. Below instruction shamt incorrect")
    valuesList.append(getBinaryShiftValue(instruction[3]))
    
    return valuesList
    
    
def getRegisterValue(reg):
    #remove any commas
    reg = reg.replace(',','')
    #create a dictionary in the future for performance
    if(reg == "$zero" or reg == "$0"):
        binaryReg = '00000'
    elif(reg == "$at" or reg == "$1"):
        binaryReg = '00001'
    elif(reg == "$v0" or reg == "$2"):
        binaryReg = '00010'
    elif(reg == "$v1" or reg == "$3"):
        binaryReg = '00011'
    elif(reg == "$a0" or reg == "$4"):
        binaryReg = '00100'
    elif(reg == "$a1" or reg == "$5"):
        binaryReg = '00101'
    elif(reg == "$a2" or reg == "$6"):
        binaryReg = '00110'
    elif(reg == "$a3" or reg == "$7"):
        binaryReg = '00111'
    elif(reg == "$t0" or reg == "$8"):
        binaryReg = '01000'
    elif(reg == "$t1" or reg == "$9"):
        binaryReg = '01001'
    elif(reg == "$t2" or reg == "$10"):
        binaryReg = '01010'
    elif(reg == "$t3" or reg == "$11"):
        binaryReg = '01011'
    elif(reg == "$t4" or reg == "$12"):
        binaryReg = '01100'
    elif(reg == "$t5" or reg == "$13"):
        binaryReg = '01101'
    elif(reg == "$t6" or reg == "$14"):
        binaryReg = '01110'
    elif(reg == "$t7" or reg == "$15"):
        binaryReg = '01111'
    elif(reg == "$s0" or reg == "$16"):
        binaryReg = '10000'
    elif(reg == "$s1" or reg == "$17"):
        binaryReg = '10001'
    elif(reg == "$s2" or reg == "$18"):
        binaryReg = '10010'
    elif(reg == "$s3" or reg == "$19"):
        binaryReg = '10011'
    elif(reg == "$s4" or reg == "$20"):
        binaryReg = '10100'
    elif(reg == "$s5" or reg == "$21"):
        binaryReg = '10101'
    elif(reg == "$s6" or reg == "$22"):
        binaryReg = '10110'
    elif(reg == "$s7" or reg == "$23"):
        binaryReg = '10111'
    elif(reg == "$t8" or reg == "$24"):
        binaryReg = '11000'
    elif(reg == "$t9" or reg == "$25"):
        binaryReg = '11001'
    elif(reg == "$k0" or reg == "$26"):
        binaryReg = '11010'
    elif(reg == "$k1" or reg == "$27"):
        binaryReg = '11011'
    elif(reg == "$gp" or reg == "$28"):
        binaryReg = '11100'
    elif(reg == "$sp" or reg == "$29"):
        binaryReg = '11101'
    elif(reg == "$fp" or reg == "$30"):
        binaryReg = '11110'
    elif(reg == "$ra" or reg == "$31"):
        binaryReg = '11111'
    else:
        binaryReg = '@@@@@'
        
    return binaryReg

def getImmediateValue(imm,numOfBits):
    
    #num of bits is 16 for immediate instructions and 26 for jump instructions
    intImm = (int(imm))
    
    if(intImm > (2**numOfBits)-1):
        print("Immediate value", imm, "too large for", numOfBits,"bits. Incorrect immediate value produced in below instruction.")
    elif(intImm < -(2**numOfBits)):
        print("Immediate value", imm, "too small for", numOfBits,"bits. Incorrect immediate value produced in below instruction.")
    
    return getTwosComplement(intImm,numOfBits)

#returns binary for shamt
def getBinaryShiftValue(shift):
    valueString = str(bin(int(shift))).replace('0b','')
    intShift = (int(shift))
    
    if(intShift<0):
        print("shift value cannot be less than 0. Below shamt is incorrect")
        return '00000'      
    else:
        if(intShift>31):
            print("The shift amount is too large to be held in 5 bits. Shamt in below instruction incorrect")
            return '00000'
        while(len(valueString)<5):
            valueString = '0' + valueString
    
    return  valueString

def findJLabelAddress(label):
    labelAddress = Labels[label]
    return getTwosComplement(labelAddress + startingAddress, 26)#add label to start address

def findBranchLabelAddress(label, currentLine):
    labelAddress = Labels[label]
    difference = (labelAddress - currentLine)-1#for offset
    return getTwosComplement(difference, 16)
    
    
def getTwosComplement(imm,numOfBits):
    intImm = (int(imm))
    twos = lambda x, count=numOfBits: "".join(map(lambda y:str((x>>y)&1), range(count-1, -1, -1)))
    
    return twos(intImm)


if __name__=="__main__":
    Labels = {}#dictionary of labels
    startingAddress = 0#default starting memory address of program
    main()
    print(Labels)