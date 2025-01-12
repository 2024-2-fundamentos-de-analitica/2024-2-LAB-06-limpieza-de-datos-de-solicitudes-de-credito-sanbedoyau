import pandas as pd
from glob import glob
import os

def pregunta_01():
    '''
    Realice la limpieza del archivo 'files/input/solicitudes_de_credito.csv'.
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en 'files/output/solicitudes_de_credito.csv'

    '''
    def create_ouptput_directory(output_directory: str):    # Función auxiliar para crear y limpiar el directorio de salida
        if os.path.exists(output_directory):
            for file in glob(f'{output_directory}/*'):
                os.remove(file)
            os.rmdir(output_directory)
        os.makedirs(output_directory)
    in_path = 'files/input'         # Path del directorio de inputs
    out_path = 'files/output'       # Path del directorio de outputs
    df = pd.read_csv(f'{in_path}/solicitudes_de_credito.csv', sep = ';', index_col = 'Unnamed: 0')      # Importar el dataframe
    df = df.dropna()                                                                                    # Eliminar registros que contienen nulos
    for column in df.columns:                                                                           # Limpieza general a cada columna
        if (df[column].dtype != object):
            continue
        df[column] = df[column].apply(lambda x: x.lower().strip().strip('-').strip('_').replace(' ', '_').replace('-', '_'))
    
    # Limpieza de la columna 'idea_negocio', donde algunos registros terminaban con 'de', 'en', 'el' o 'y', por lo que se eliminan estas últimas palabras
    df['idea_negocio'] = df['idea_negocio'].apply(lambda x: '_'.join(x.split('_')[:-1]).strip('_') if x.split('_')[-1] in ('de', 'en', 'el', 'y') else x)

    # Limpieza de la columna 'barrio', donde los registros conflictivos son los siguientes:
    # - Algunos barrios tienen numerales. Por ejemplo bombona no 1. El problema es que algunos están escritos como no. 1, y otros sin espacio
    # - El barrio belen, tiene tilde (é), cosa que puede causar conflicto en la codificación, remplazando é por ¿, por lo que se hace el remplazo nuevamente, sin tilde
    # - El barrio antonio nariño tiene un problema similar a belen, pero con la ñ, por lo que también se hace el inverso
    # - El resto de barrios se les limpian posibles . que puedan contener
    #df['barrio'] = df['barrio'].apply(lambda x: str(x).replace('no._', 'no.').replace('no.', 'no_').replace('.', ''))

    # Se cambia el tipo de las columnas 'estrato' y 'comuna_ciudadano' (irrelevante)
    df['estrato'] = df['estrato'].astype(int)
    df['comuna_ciudadano'] = df['comuna_ciudadano'].astype(int)

    # Limpieza de la columna 'fecha_de_beneficio', donde algunos registros están en formato YYYY/MM/DD y otros DD/MM/YYYY, por  lo que todas quedan con el formato DD/MM/YYYY
    df['fecha_de_beneficio'] = df['fecha_de_beneficio'].apply(lambda x: '/'.join([y for y in reversed(x.split('/'))]) if len(x.split('/')[0]) == 4 else x)

    # Limpieza de la columna 'monto_del_credito' donde hay algunos espacios en blanco (que fueron remplazados con _), signos de $ y . al final
    # además de tener , como separador de miles. Los datos se limpian de tal forma que se pueden convertir en tipo entero
    df['monto_del_credito'] = df['monto_del_credito'].apply(lambda x: str(x).replace('_', '').replace('$', '').split('.')[0].replace(',','')).astype(int)

    # Limpieza de la columna 'línea_credito' donde hay algunos espacios en blanco (que fueron remplazados con _) 
    # o palabras con una división poco coherente, por lo que se corrige
    df['línea_credito'] = df['línea_credito'].apply(lambda x: str(x).replace('_', ' ').replace('cap.', 'cap '))
    df = df.drop_duplicates()       # Eliminar valores duplicador
    create_ouptput_directory(out_path)
    df.to_csv(f'{out_path}/solicitudes_de_credito.csv', sep = ';')
    print(len(df['barrio'].unique().tolist()))

# cordoba

pregunta_01()