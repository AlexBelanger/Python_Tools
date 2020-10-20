import os, time

def timedeco(func):
    def wrapper(*args, **kwargs):
        start = time.process_time()
        rv = func(*args, **kwargs)
        elapse =time.process_time()-start
        print(f"Func {func.__name__} took {elapse} ns")
        return rv
    return wrapper

wd = True

# if wd is True:
#     workingdirectory = os.getcwd()
# else:
#     workingdirectory = wd

workingdirectory = os.getcwd() if wd else wd

print(f"\nWD = {workingdirectory}")

data = 100000

@timedeco
def f(x):
    sum = 0
    for i in range(x):
        sum +=i**2
    return sum

ans = [f(data),f(data)**2]
print(f"Ans = {ans}")
ans2 = [y:=f(data),y**2]
print(f"Ans2 = {ans2}")


def add2(x):
    return x+2

add2 = timedeco(add2)
ans3 = add2(2)
ans4 = timedeco(add2)(2)
print(ans3)
print(ans4)

def runN(n):
    def timedeco(func):
        def wrapper(*args, **kwargs):
            start = time.process_time()
            for i in range(n):
                rv = func(*args, **kwargs)
            elapse =time.process_time()-start
            avg = elapse/float(n)
            print(f"Func {func.__name__} took on average {avg} ns")
            print(f"Func {func.__name__} took a total {elapse} to complete {n} times")
            return rv
        return wrapper
    return timedeco

@runN(10000)
def add5(x):
    return x+5
ans5 = add5(5)
