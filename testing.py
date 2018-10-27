a = ['.exe', '.py', '.bat']

file = 'getRun.exe'

print(file.index('.'))
print(file[file.index('.'):-1] + file[-1])
if file[file.index('.'):-1] + file[-1] in a:
    print("yes")

if "." in file:
    print("yes again")

depth = 1
structure = ['data', 'customer*', 'projects*', 'modules*']
print(len(structure[depth][:-1])-1)

x = []
for i in range(0,10):
    x.append(i)