import csv
from unidecode import unidecode


def get_stations_pos():
    stations = dict()

    with open('./emplacement-des-gares-idf-data-generalisee.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        i = 1
        k = []
        for row in reader:
            if i == 1:
                i += 1
                continue
            t = row[0].split(';')[1].split(': ')[1].strip('], ""type""').strip('[').split(', ')
            t.append(row[0].split(';')[4])
            k.append(t)

        with open("./graphs/metro correspondences vertices", 'r', encoding='utf-8') as f:
            line = f.readline()
            while line != "":
                l_temp = line.strip('\n').split('\t')

                v = 0
                for elt in k:
                    if elt[2] in ["Lisière Pereire"]:
                        continue
                    if "".join(map(lambda c: c if c != " " else "", unidecode(l_temp[1]))).lower().replace("-", "") == "".join(map(lambda c: c if c != " " else "", unidecode(elt[2]))).lower().replace("-", ""):
                        stations[int(l_temp[0])] = (float(elt[1]), float(elt[0]))
                        v += 1
                        """elif "".join(map(lambda c: c if c != " " else "", unidecode(elt[2]))).lower().replace("-", "") in "".join(map(lambda c: c if c != " " else "", unidecode(l_temp[1]))).lower().replace("-", ""):
                        stations[int(l_temp[0])] = (float(elt[1]), float(elt[0]))
                        v += 1"""
                    else:
                        for test in ["Mitterrand", "Porte Maillot", "Pont de Levallois", "Pereire", "Montparnasse", "Javel", "Les Courtilles"]:
                            if test in elt[2] and test in l_temp[1]:
                                stations[int(l_temp[0])] = (float(elt[1]), float(elt[0]))
                                v += 1
                                break
                assert v < 2, f"impossible ! station n°{l_temp[0]} '{l_temp[1]}' matched to {v} different stations in idf csv."
                assert len(stations)-1 == int(l_temp[0]), f"impossible !! station n°{l_temp[0]} '{l_temp[1]}' was not found automatically in idf csv. Need manual fix."

                line = f.readline()

    return stations


def get_all_stations_pos():
    stations = dict()

    with open('./emplacement-des-gares-idf-data-generalisee.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        i = 1
        j = 0
        for row in reader:
            if i == 1:
                i += 1
                continue
            t = row[0].split(';')[1].split(': ')[1].strip('], ""type""').strip('[').split(', ')
            t.append(row[0].split(';')[4])

            stations[(int(j), t[2])] = (float(t[1]), float(t[0]))
            j += 1

    return stations
