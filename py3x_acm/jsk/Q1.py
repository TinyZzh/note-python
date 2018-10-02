
if __name__ == "__main__":
    try:
        while True:
            a, b, c = map(int, input().split())
            print(a + b + c)
    except EOFError:
        pass
