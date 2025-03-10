import sys

if len(sys.argv) < 2:
    print("USAGE: python AutoItSwitchCleaner.py [FILENAME]")
    sys.exit(0)

file = open(sys.argv[1],"r").read().splitlines()
result = open("result.au3","a")

cache = ""
insideSwitch = False
switch_counter = 0
switch_index = 0
end_index = 0
foundEndLoop = False
last_case = 0
important_case = 0

for num in range(len(file)):
    if num + 1 < len(file) and file[num] == "Do" and file[num+1].startswith("Switch "):
        switch_counter += 1
        insideSwitch = True
        switch_index = num-2
        
    if not insideSwitch and num + 1 < len(file) and not file[num+1] == "Do" and not file[num+2] == "Do":
        result.write(file[num]+"\n")
    
    if file[num].startswith("Case"):
        last_case = num
        
    if file[num] == "ExitLoop":
        foundEndLoop = True
        important_case = last_case
        end_index = num
        
    if file[num].startswith("Until"):
        for i in range(important_case+1, end_index):
            result.write(file[i]+"\n")

        insideSwitch = False
        
    if file[num] == "EndFunc":
        result.write("\n#comments-start \n End of a Function \n #comments-end \n")

    if num + 1 < len(file) and file[num+1].startswith("Func "):
        result.write("\n#comments-start \n Start of a Function \n #comments-end \n")
    
print("Found "+ str(switch_counter) + " statements")
print("Final result is written to: result.au3")
result.close()
    
