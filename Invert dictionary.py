def group_by_owners(files):
    owners = {}
    for k, v in files.items():
        if v not in owners.keys():
            owners[v] = []
    
    for k, v in files.items():
        owners[v].append(k)
    
    return owners
    
files = {
    'Input.txt': 'Randy',
    'Code.py': 'Stan',
    'Output.txt': 'Randy'
}   
print(group_by_owners(files))