

if __name__ == "__main__":
    while True:
        var0 = input()
        end_index = int(len(var0) / 2)
        x_ind = end_index if len(var0) % 2 == 0 else end_index + 1
        print("Yes" if var0[0:end_index] ==
              var0[x_ind:len(var0)][::-1] else "No")
