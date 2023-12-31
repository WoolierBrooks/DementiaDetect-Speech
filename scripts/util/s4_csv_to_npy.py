import pandas as pd
import numpy as np

data = pd.read_csv("<diretório do arquivo .txt>", sep=' ', header=None)
data_npy = data.values

# Use a função numpy.isnan() para identificar as posições com NaN
nan_indices = np.isnan(data_npy)

# Use a indexação booleana para manter apenas os valores sem NaN
data_npy_sem_nan = data_npy[~nan_indices]

altura = data_npy_sem_nan.shape[0]
print("Altura:", altura)

# Salvar apenas os valores sem NaN no arquivo "hi.npy"
np.save("teste.npy", data_npy_sem_nan)