
# Q18: https://nanti.jisuanke.com/t/18

if __name__ == "__main__":
    try:
        while True:
            var0 = eval(input())
            var1 = list(map(int, input().split()))

            index = 0
            while index < var0 and var1[index] != 0:
                index += var1[index]
                if index == var0 - 1:
                    break

            print('true' if index == var0 - 1 else 'false')
    except EOFError:
        pass
