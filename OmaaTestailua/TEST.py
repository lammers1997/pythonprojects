def mystery1(A, B):
    res = 0
    while B > 0:
        if B % 2 == 1:
            res = res+A
        A = A*2
        B=B//2

    if res == 0:
        return A
    else:
        return res



def main():
    print(mystery1(4, 3))
    print(mystery1(1,1))
    print(mystery1(1,2))
    print(mystery1(1,3))

    print(mystery1(3,3))
    print(mystery1(3,4))
    print(mystery1(3,5))
    print(mystery1(3,6))

if __name__ == "__main__":
    main()