# Durante o periodo de seca as queimadas prejudicam muito o ar,
# dai pensei, como seria um sistema que medisse o cO2 nestas regiões.
# Cada cidade conta com  sensores
# O nivel normal de cO2 seria de  350.
# O nivel atual do cO2 será a media capitada pelos 05 sensores
# Caso a media atinja 450, dai em diante o sistema alerta para critico.
# Pegando como referencia as cidades de Brasilia, teremos .

print('********** SISTEMA DE MEDIÇÃO DE cO2 ATMOSFERICO **********')
niveis_cO2 = {
    'Planaltina': [330, 440, 550, 498, 650], 
    'Paranoa':   [456, 650, 440, 350, 498],
    'Esplanada':  [350, 386, 456, 654, 356],
    'Ceilandia':  [123, 456, 654, 489, 455],
    'Sobradinho': [123, 321, 345, 543, 542],
    }
for cidade in niveis_cO2:
    qtde_sensores = len(niveis_cO2[cidade])
    total_cO2 = sum(niveis_cO2[cidade])
    media_cO2 = total_cO2 / qtde_sensores
    if media_cO2 > 450:
        print('A cidade de: {} está com nivel de cO2 de: {} :!'.format(cidade, media_cO2))
    else:
        pass