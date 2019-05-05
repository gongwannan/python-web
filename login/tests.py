from django.test import TestCase

# Create your tests here.
l = ['a','1','A','w']

for i in range(len(l)-1):
    for n in range(len(l)-i-1):
        if l[n] < l[n+1]:
            l[n], l[n+1]=l[n+1], l[n]
print(l)