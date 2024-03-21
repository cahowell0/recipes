text = open('new_text.txt', 'r')

with open('new_new_text.txt', 'w') as file:
    for t in text:
        t = t.replace('.000000000000000000e+00', '')
        t = t.replace(' ', '')

        file.writelines(t)   