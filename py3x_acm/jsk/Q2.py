
if __name__ == "__main__":
    try:
        while True:
            a, b = map(int, input().split())

            print("YES" if b == 1 or a % b == 0 else "NO")
    except EOFError:
        pass
    except:
        pass
