import numpy as np
import re
arr = ['Jonas Karlsson', '3 recensioner', '\ue5d4', '\ue838', '\ue838', '\ue838', '\ue838', '\ue838', 'för 3 månader sedan', 'Super otrevlig personal! Vi var där 10 Augusti efter cykelvasan, hade beställt 4 pizzor, 2 med sås, den ena pizzan skulle vara med sås på, vi får 2 burkar brevid, vi ber snäll om han kan hälla på såsen, får ett otrevligt svar tebax, Spelar det någon roll? Uppenbarligen annars hade vi ju ej ställt frågan, frågar om sallad ingår men det gjorde det inte! När vi kom hem var pizzan dränkt i sås, in direkt oätlig! Aldrig den pizzerian igen!!!!', 'Mat: 1', 'Tjänst: 1', 'Atmosfär: 1', '\ue8dc', 'Gilla', '\ue80d', 'Dela']
for i, el in enumerate(arr):
    arr[i] = (re.sub('[^A-Za-z0-9åäöÅÄÖ.,\s]+', '', el))

new_arr = []
for i, el in enumerate(arr):
    if el != '':
        new_arr.append(el)
print(new_arr)


# for i,char in enumerate(string):
#     if char == '':
#         print(char)
#         string[:i] + string[i + 1:]
# print(string.split(''))
# print(string.split(''))