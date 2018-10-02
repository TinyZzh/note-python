

def is_prime_num(numeric):
    for i in range(2, numeric):
        if numeric % i == 0:
            return False
    return True


if __name__ == "__main__":
    try:
        while True:
            var0 = int(eval(input()))
            print("YES" if is_prime_num(var0) else "NO")
    except EOFError:
        pass
    except:
        pass
