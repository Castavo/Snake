def download(mode):
    with open("saves.txt") as file:
        s = file.read()
        i0, i, n = 0, 0, len(s)
        while i < n:
            if s[i] == ':' and s[i0: i - 1] == mode:
                i0 = i

            elif s[i] == '\n' and s[i0] == ':':
                return int(s[i0 + 1: i])

            elif i == n - 1 and s[i0] == ':':
                return int(s[i0 + 1: i + 1])

            elif s[i] == '\n':
                i0 = i + 1
            i += 1
        if i == n:
            return 0


def upload(mode, score):
    with open("saves.txt") as file:
        s = file.read()
        sent, i0, i, n = True, 0, 0, len(s)
        while sent and i < n:
            if s[i] == ':' and s[i0: i - 1] == mode:
                i0 = i

            elif (s[i] == '\n' or i == n - 1) and s[i0] == ':':
                sent = False

            elif s[i] == '\n':
                i0 = i + 1
            i += 1

    with open("saves.txt", 'w') as file:
        if sent:
            file.write(s + '\n' + mode + ' : ' + str(score))
        else:
            file.write(s[:i0 + 2] + str(score) + s[i - 1:])