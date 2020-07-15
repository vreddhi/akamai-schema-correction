import json
import sys
import argparse
import os

#Add parser arguments
parser = argparse.ArgumentParser()
parser.add_argument("-directory",help="location of templates directory")
args = parser.parse_args()

if not args.directory:
    print("Missing OR wrong arguments. Use -h for help options")
    exit()


def getChildRulesandUpdate(parentRule):
    for eachRule in parentRule:
        for eachcriteria in eachRule['criteria']:
            if eachcriteria['name'] == 'path':
                if 'normalize' not in eachcriteria['options'].keys():
                    eachcriteria['options']['normalize'] = False
                    print('Adding normalize option in rule: ' + eachRule['name'])
            else:
                pass
        #Check whether we have child rules, where in again criteria might be found
        if len(eachRule['children']) != 0:
            getChildRulesandUpdate(eachRule['children'])
    #Awesome, we are done updating criterias, lets go back
    return parentRule

directory = args.directory
for root, dirs, files in os.walk(directory):
    for each_file in files:
        if each_file.endswith('.json'):
            #print(each_file)
            input_file = os.path.join(directory, each_file)
            print('\nProcessing: ' + input_file)
            with open(input_file, mode='r') as FileHandler:
                file_content = FileHandler.read()
            jsonContent = json.loads(file_content)
            if 'rules' in jsonContent:
                #print('\nThis will not work for main.json\n')
                pass
            else:
                cleanContent = getChildRulesandUpdate([jsonContent])
                #print(json.dumps(cleanContent[0], indent=4))
                try:
                    with open(input_file, 'w') as outputFile:
                        outputFile.write(json.dumps(cleanContent[0], indent=4))
                except FileNotFoundError:
                    print('\n Unable to write output\n')
        else:
            print('\n Skipping ' + each_file + '\n')   
            pass

print('******************************************************************')
print('NOTE: This script does not work for main.json. Work on it manually')
print('******************************************************************\n')
