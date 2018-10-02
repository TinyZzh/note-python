
if __name__ == "__main__":
    try:
        while True:
            size = int(input())
            arys = map(str, input().split())
            num = int(''.join(list(arys))) + 1
            print(" ".join(list(str(num))))
    except EOFError:
        pass
