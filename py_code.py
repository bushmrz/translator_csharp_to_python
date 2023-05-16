a = 10
a = 20
b = "20"
abs = "c"
count = 0
def something():
    print("Hello")

print("Test calling function that prints Hello")
something()
c = 10
print("Test: 10 + 10:")
print(a + c)
arr = [1, 2, 3, 2, 3, 4]
print("Printing arr = [1, 2, 3, 2, 3, 4]:")
print(arr)
print("Printing arr[1]:")
print(arr[1])
print("Changing arr[1] to 20:")
arr[1] = 20
print(arr[1])
testBool = True
testBool2 = False
if ((testBool && testBool2) || False):
    print("if went to true")
else:
    print("if went to false")

count1 = 2
while count < 5:
    count = 1
count1 = 2

print(count)
print(count1)
class Some:
    def sum(a, b):
        return a + b
    

class Something(Some):
    def test():
        print("Calling parent class method:")
        sumResult = super.sum(10, 5)
        print(sumResult)
    

Something().test()
class EmptyClass:
    pass
