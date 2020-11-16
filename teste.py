a = "eu amo comer muito bolo"

a = a.split()
print(a[3])
print(','.join(a[:3]) + "," + ','.join(a[4:]))