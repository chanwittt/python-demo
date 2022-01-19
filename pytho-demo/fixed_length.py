f = open("src.txt", "r")
data = f.read()
# max-width per column, column == key, width == value
w = {}
lines = data.splitlines()
for line in lines:
    for col_nr, col in enumerate(line.strip().split(",")):
        w[col_nr] = max( w.get(col_nr,0), len(col))

# write file
with open("test_fixed.txt","w") as ff:
    for line in lines:
        for col_nr, col in enumerate(line.strip().split(",")):
            # the :<{w[col_nr]+5}} - part is left-adjusting to certain width 
            #f.write(f"{col:<{w[col_nr]+5}}") # 5 additional spaces
            if col_nr == 0:
                ff.write(f"{col:<{'16'}}")
                print('length16')
            else:
                ff.write(f"{col:<{'14'}}")
                print('length14')
            #print(col[0:15]+str(col_nr))
        ff.write("\n")

#with open("test_fixed.txt","r") as f:
    #print(f.read())

