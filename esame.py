#le eccezioni da alzare in caso di imput non correnti o casi limite devono essere istanze di una specifica classe ExamException
class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    def __init__(self, name):
        self.name = name

    def get_data(self):
        try:
            my_file = open(self.name, 'r')
            lines = my_file.readlines()
            lines = lines[1:]
            my_file.close()

        # Nel caso il file non esista o non sia leggibile alzo un'eccezione
        except Exception as e:
            raise ExamException('Errore in apertura del file')

        lista = []

        # Inizializzo una variabile old_line_list per memorizzare la riga precedente del file
        old_line_list = None

        for line in lines:
            # Suddivido la riga in una lista di elementi separati dalla virgola
            line_list = line.split(',')

            line_list = [line.strip() for line in line_list]

            if len(line_list) < 2:
                continue

            if len(line_list) > 2:
                line_list = line_list[:2]

            # Controllo che la data sia nel formato corretto YYYY-MM (isdigit controlla che le stringhe siano composte da cifre)
            if not (len(line_list[0]) == 7 and line_list[0][:4].isdigit() and line_list[0][4] == '-' and line_list[0][5:].isdigit()):
                # Salto la riga
                continue
            
            # Definisco anno e mese correnti in due variabili intere
            anno_corrente, mese_corrente = [int(part) for part in line_list[0].split('-')] 
            
            # Controllo che il mese sia compreso tra 01 e 12                
            if mese_corrente < 1 or mese_corrente > 12:
                continue
            
            if old_line_list is not None:
                # Verifico che non ci siano date duplicate
                if line_list[0] == old_line_list[0]:
                    raise ExamException(f'Ci sono delle date duplicate: {old_line_list[0]}, {line_list[0]}')
                
                # Definisco anno e mese vecchi in due variabili intere
                old_year, old_month = [int(part) for part in old_line_list[0].split('-')]
                
                # Verifico che le date siano in ordine, altrimenti alzo un'eccezione
                if old_year == anno_corrente and old_month > mese_corrente:
                    raise ExamException(f'I mesi delle date non sono in ordine: {old_line_list[0]}, {line_list[0]}')
                if old_year > anno_corrente:
                    raise ExamException(f'Gli anni delle date non sono in ordine: {old_line_list[0]}, {line_list[0]}')

            old_line_list = line_list

            # Il primo elemento della lista lo associo a 'date' e il secondo a 'passengeri'
            data, passeggeri = line_list
            
            # Togli spazi e a capo all'inizio e alla fine (in 'data')
            data = data.strip() 
            
            # Controllo che il numero di passeggeri sia un intero positivo
            try:
                passeggeri = int(passeggeri.strip())
            except:
                continue

            if passeggeri <= 0:
                continue
            
            # Aggiungo una lista contenente data e numero di passeggeri
            lista.append([data, passeggeri])

        # Ritorno una lista di liste  
        return lista

# Creo un funzione che ha come imput la time series
def find_min_max(time_series):

    if time_series == []:
        return {}
    
    # Inizializzo un dizionario vuoto per memorizzare i risultati
    data = {}

    #Inizializzo una lista vuota per memorizzare in posizione '0' gli anni, e in '1' le righe dello stesso anno
    lista_anni = []
    
    # Estraggo il primo e l'ultimo anno dalla time series
    primo_anno = time_series[0][0].split('-')[0]
    ultimo_anno = time_series[-1][0].split('-')[0]

    # Itero attraverso gli anni compresi tra il primo e l'ultimo inclusi e li trasfrmo in interi
    for anno in range(int(primo_anno), int(ultimo_anno) + 1):

        # Lista vuota dove metterò le liste [anno-mese,passeggeri] tutte dello stesso anno
        lista_anno = []

        for item in time_series:
            # Trasformo in interi la prima parte (anno) separato dal mese con "-"
            item_anno = int(item[0].split('-')[0])

            if item_anno == anno:
                lista_anno.append(item)

        lista_anni.append([anno, lista_anno])

    # anno =[anno , [lista]]
    for anno in lista_anni:
        if len(anno[1]) == 0:
            continue
        
        # Creo il dizinario con chiave 'anno' (in stringa) e come valori il dizionario con chiavi 'min' e 'max' (in stringa)
        data[str(anno[0])] = {"min": [], "max": []}

        # Trovo min e max tra i passeggeri
        min_pass = min([item[1] for item in anno[1]]) #anno[1]=[data,passeggeri]  item[1]=passeggeri
        max_pass = max([item[1] for item in anno[1]])
        
        for item in anno[1]:
            # Se l'elemento 1 (passeggeri) è uguale al min/max dei passeggeri,aggiungo il mese associato come valore alla chiave 'min/max'
            if item[1] == min_pass:
                data[str(anno[0])]['min'].append(item[0].split('-')[1]) #item[0]=data

            if item[1] == max_pass:
                data[str(anno[0])]['max'].append(item[0].split('-')[1])

    # Ritorno un dizionario di dizionari
    return data

