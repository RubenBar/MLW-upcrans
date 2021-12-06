#!/usr/bin/python
# coding: utf-8
######################
# Obfuscating another python file
######################

import sys
import argparse
import re
import random
import string
import os

reservedWords = ['False','def','if','raise',
                    'None','del','import','return',
                    'True','elif','in','try','and',
                    'else:','is','while','as',
                    'except','lambda','with',
                    'assert','finally','nonlocal',
                    'yield','break','for','not',
                    'class','from','or','continue','global','pass','extensions']

def randomASCII(length=8):
    return ''.join(random.choice(string.ascii_letters) for i in range(length)) 

def addEntropyToName(name):
    #result = name + randomASCII(5)
    result = randomASCII(10)
    return result 

def deadParameter():
    randomParameter = randomASCII()
    randomValue = randomASCII()
    deadLine = "{} = '{}'".format(randomParameter, randomValue)
    return deadLine

def indent(text, amount, ch=' '):
    padding = amount * ch
    return ''.join(padding+line for line in text.splitlines(True))

def deadConditional():
    operand_types = [ "==", "<=", "<"]
    conditionals = [ "and", "or" ]
    condition = ""
    for i in range(random.randint(1, 3)):
        condition += " ({} {} {}) ".format(random.randint(1,100000000), random.choice(operand_types), random.randint(1,1000000))
    condition = condition.replace("  ", " " + random.choice(conditionals) + " ").strip()
    randomData = deadParameter()
    junk = "if ({}):\n    {}\n".format(condition,randomData)
    return junk

def deadLoop():
    for_var = ''.join([random.choice(string.ascii_letters) for n in range(random.randint(5, 10))])
    randomParameter = randomASCII()
    randomBoolean = random.choice([ "True", "False" ])
    junk = "for {} in range ({}): \n".format(for_var, random.randint(1, 10))
    junk +="    {} = {}\n".format(randomParameter, randomBoolean)
    for i in range(random.randint(1,2)):
        deadSatetement = deadParameter();
        junk +="    {}\n".format(deadSatetement)

    return junk
  
def isBlankLineOrComment(line):
    result = False
    if(line.startswith('#')):
        result = True
    if not line.strip():
        result = True
    return result

def getLeadingSpaces(text):
    return len(text) - len(text.lstrip())

def methodNames(infilename, outfilename, debug=True):

    methodDir = {}

    with open(outfilename, 'w') as outfile, open(infilename , 'r') as infile:

        pattern='^def\s*(.*)\(.*\):\s*$'

        for line in infile:

            if line.startswith('#'):
                outfile.write(line)
                continue

            if line.startswith('import'):
                outfile.write(line)
                continue

            lineToWrite = line
            
            result = re.search(pattern, line)
            
            if(result):

                # Get if I can rename sth and add it to the dictionary
                print("Found method name to obfuscate: {}".format(result.group(1))) if debug else None

                methodName = result.group(1)
                
                if not(methodName == 'parse_args'):
                  # Add entropy to the method
                  newmethodName = addEntropyToName(methodName)

                  # Add it to the dictionary
                  methodDir[methodName] = newmethodName

                  lineToWrite = line.replace(methodName, newmethodName)
            else:
                # See if an existing rule applies and change it
                for originalmethodName, newmethodName in methodDir.items():
                    
                    if (originalmethodName + "(") in lineToWrite:
                        if not ("."+originalmethodName + "(") in lineToWrite:
                            lineToWrite = line.replace(originalmethodName, newmethodName)
            
            outfile.write(lineToWrite)
    return

def isVariableName(name):

    result = True
    if(name in reservedWords):
        result = False
    if name.startswith('"') or name.startswith('`') or name.startswith('\'') or name.startswith("'") or name.startswith("]") or name.startswith("elif"):
        result = False
    if name.endswith('(') or name.endswith(')'):
        result = False
    
    return result

def getVariableListFromString(input):
    result = []
    for i in input.split(','):
        if i:
            result.append(i.strip().split('=')[0].split(':')[0])

    result.sort(reverse=False)

    return result

def variableNames(infilename, outfilename, debug=False):
    isMethodBody = False

    with open(outfilename, 'w') as outfile, open(infilename , 'r') as infile:
        for line in infile:

            if line.startswith('#'):
                outfile.write(line)
                continue

            if line.startswith('import'):
                outfile.write(line)
                continue

            lineToWrite = line

            identation = getLeadingSpaces(line)

            if(identation == 0 and not isBlankLineOrComment(line)):
                isMethodBody=False

            pattern='^def\s*(.*)\((.*)\):\s*$'

            result = re.search(pattern, line)
            
            if(result):

                if(result.group(1) == 'main'):
                    outfile.write(lineToWrite)
                    continue

                varDir = {}
                isMethodBody = True

                variableListAsString = result.group(2)

                variableList = getVariableListFromString(variableListAsString)

                if(debug):
                    if(len(variableList) > 0):
                        print("Variables discovered in function {}: {}".format(result.group(1),variableList))
                    else:
                        print("No variables discovered in function {}".format(result.group(1)))

                for variable in variableList:
                    varDir[variable] = addEntropyToName(variable)
                    lineToWrite = lineToWrite.replace(variable, varDir[variable])
            else:
                if(isMethodBody and not len(variableList) == 0):
                    # See if an existing rule applies and change it
                    for originalVarName, newVarName in varDir.items():
                        if not originalVarName in lineToWrite:
                            continue

                        checkForAdditionalUpdate = True
                        dynamicPattern = '(^'+originalVarName+'\W+|\W+'+originalVarName+'\W+|\W+'+originalVarName+'$)'

                        #Cover the corner case where two identical variables are next to each other
                        while (checkForAdditionalUpdate):
                            results = re.findall(dynamicPattern, lineToWrite)
                            print("Found {} occurence(s) of the original variable {} in line {}. Should change it to {}in line".format(len(results), originalVarName, lineToWrite, newVarName)) if debug else None
                            for result in results:
                                newEntry = result.replace(originalVarName, newVarName)
                                lineToWrite = lineToWrite.replace(result, newEntry)

                            if not results:
                                checkForAdditionalUpdate = False
            
            outfile.write(lineToWrite)
    return

def addCode(infilename, outfilename, debug=False):
    isMethodBody = False
    with open(outfilename, 'w') as outfile, open(infilename , 'r') as infile:
        for line in infile:
            if line.startswith('#'):
                outfile.write(line)
                continue

            if line.startswith('import'):
                outfile.write(line)
                continue

            lineToWrite = line

            identation = getLeadingSpaces(line)

            if(identation == 0 and not isBlankLineOrComment(line)):
                isMethodBody=False

            pattern='^def\s*(.*)\((.*)\):\s*$'

            result = re.search(pattern, line)
            deadParameterList = []
            randomStatement = deadParameter()
            randomConditional = deadConditional()
            randomLoop = deadLoop()

            if(result):
                
                if(result.group(1) == 'main' or result.group(1) =='create_Readme'):
                    outfile.write(lineToWrite)
                    continue
                
                isMethodBody = True
                outfile.write(lineToWrite)
            else:
                if(isMethodBody):
                    skipVariable = isVariableName(lineToWrite.strip())

                    if skipVariable and not isBlankLineOrComment(line):
                        deadParameterList.append(randomStatement)
                        deadParameterList.append(randomConditional)
                        deadParameterList.append(randomLoop)
                        junk = random.choice(deadParameterList)
                        randomParameterToWrite = indent(junk, identation)
                        outfile.write(randomParameterToWrite+"\n")
                
                outfile.write(lineToWrite)
    return

def shuffleMethods(infilename, outfilename, debug=False):

    isMethodBody=False
    methodBodyLines=[]
    methodsList=[]

    importCodeLines=[]
    remainingCodeLines=[]

    #Load methods to memory
    with open(infilename , 'r') as infile:
        for line in infile:
            line = line.rstrip('\n')
            if line.startswith('#'):
                remainingCodeLines.append(line)
                continue

            if line.startswith('import'):
                importCodeLines.append(line)
                continue

            identation = getLeadingSpaces(line)

            if(identation == 0 and not isBlankLineOrComment(line)):
                if(len(methodBodyLines) != 0):
                    print("Adding method {} to the list".format(methodBodyLines[0]))
                    methodsList.append(methodBodyLines)
                    methodBodyLines = []
                isMethodBody=False

            pattern='^def\s*(.*)\((.*)\):\s*$'

            result = re.search(pattern, line)
            
            if(result):
                isMethodBody = True
                print("New method definition {}".format(result.group(0))) if debug else None
                methodBodyLines = [result.group(0)]
            else:
                if(isMethodBody):
                    methodBodyLines.append(line)
                else:
                    remainingCodeLines.append(line)
        #Any remaining block must be added to the methodsList
        if(len(methodBodyLines) != 0):
            methodsList.append(methodBodyLines)

    print("Before Shuffling {}".format(methodsList)) if debug else None

    #Shuffle method order
    random.shuffle(methodsList)

    print("After Shuffling {}".format(methodsList)) if debug else None

    #Create obfuscated file (first the methods then the remaining code)
    with open(outfilename, 'w') as outfile:

        for codeLine in importCodeLines:
            outfile.write(codeLine+"\n")

        for methodBody in methodsList:
            for codeLine in methodBody:
                outfile.write(codeLine+"\n")
            outfile.write("\n")

        for codeLine in remainingCodeLines:
            outfile.write(codeLine+"\n")      

    return

def obfuscationManager(infile, outfile, mode, debug=False):
    
    if(mode == 'method-names'): 
        methodNames(infile, outfile, debug)
    elif(mode == 'variable-names'):
        variableNames(infile, outfile, debug)
    elif(mode == 'add-code'):
        addCode(infile, outfile, debug)
    elif(mode == 'shuffle-methods'):
        shuffleMethods(infile, outfile, debug)
    else:
        addCode(infile, infile+".tmp1", debug)
        methodNames(infile+".tmp1", infile+".tmp2", debug)
        variableNames(infile+".tmp2", infile+".tmp3", debug)
        shuffleMethods(infile+".tmp3", outfile, debug)
        os.remove(infile+".tmp1")
        os.remove(infile+".tmp2")
        os.remove(infile+".tmp3")
    return

def main(*args):
    desc = """
    This is a parser to obfuscate a python script and store it to a different file
    """
    elog = "Example：obfuscate.py --file <filename.py> --out <out file> --mode <mode of obfucation>?"

    parser = argparse.ArgumentParser(description=desc, epilog=elog)

    parser.add_argument('-f', '--file', help='Provide the input file that needs to be obfuscated ', required=True, dest='infile')

    parser.add_argument('-o', '--out', help='Provide the output file that will be generated ', required=True, dest='outfile')

    parser.add_argument('-m', '--mode', nargs='?', default='method-names',
                        help='Obfuscation moded: 1. Change method names 2. Change variable names 3. Introduce meaningless code blocks. The default is method names',
                        dest='mode', choices=['method-names', 'variable-names', 'add-code', 'shuffle-methods', 'all'])

    parser.add_argument('-d', '--debug', dest='debug', action='store_true')

    if len(sys.argv) < 2:
        parser.print_help()
        return
    args = parser.parse_args()

    #if args.mode.lower() == "add-code":
        #print("[-]Currently only method-names mode is supported.")
        #return

    obfuscationManager(args.infile, args.outfile, args.mode.lower(), args.debug)

if __name__ == '__main__':
    main()
