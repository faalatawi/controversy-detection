# Read a file
file_name = "generateDataForVenezuelaPolarizationScore.py"
output = file_name[:-3] + "_clean.py"


lines = []
with open(file_name, "r") as f:
    lines = f.readlines()

with open(output, "w") as f:
    for line in lines:
        # relpace every 4 spaces with 1 tab
        line = line.replace("    ", "\t")

        # if line contains "print" replace it with "print("
        if "print" in line:
            line = line.replace("print", "print(")
            line = line.replace("\n", ")")
            line += "\n"

        f.write(line)
