import os
import numpy as np
from tslearn.utils import to_time_series_dataset
from tslearn.neighbors import KNeighborsTimeSeriesClassifier
from sklearn.model_selection import train_test_split, KFold, GridSearchCV

# Carregar dados de pacientes com diagnóstico de demência positivo
folder_dementia = r"C:\Users\Lenovo\Desktop\IC\[99] Database Final (160)\cookie_d"
data_dementia = []
for npy_file in os.listdir(folder_dementia):
    if npy_file.endswith(".npy"):
        data = np.load(os.path.join(folder_dementia, npy_file))
        data_dementia.append(data)
data_dementia = np.array(data_dementia, dtype=object)

# Carregar dados de pacientes con diagnóstico de demência control (controle)
folder_control = r"C:\Users\Lenovo\Desktop\IC\[99] Database Final (160)\cookie_c/"
data_control = []
for npy_file in os.listdir(folder_control):
    if npy_file.endswith(".npy"):
        data = np.load(os.path.join(folder_control, npy_file))
        data_control.append(data)
data_control = np.array(data_control, dtype=object)

# Combinar e etiquetar os dados
X_train = np.concatenate((data_dementia, data_control), axis=0)
y_train = np.concatenate((np.ones(len(data_dementia)), np.zeros(len(data_control))), axis=0)

# Dividir os dados em treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Converter para o formato correto de séries temporais
X_train = to_time_series_dataset(X_train)
X_test = to_time_series_dataset(X_test)

# Definir os hiperparâmetros para a busca em grade
p_grid = {"n_neighbors": [1, 5]}

# Definir o método de validação cruzada
cv = KFold(n_splits=2, shuffle=True, random_state=0)

# Criar o classificador KNN
knn = KNeighborsTimeSeriesClassifier(metric="dtw")

# Criar o objeto para busca em grade
clf = GridSearchCV(estimator=knn, param_grid=p_grid, cv=cv)

# Treinar o modelo com busca em grade
clf.fit(X_train, y_train)

# Obter os melhores hiperparâmetros encontrados
best_params = clf.best_params_
print("Melhores hiperparâmetros:", best_params)

# Obter o modelo com os melhores hiperparâmetros
best_knn = clf.best_estimator_

# Fazer a previsão com o modelo treinado com os melhores hiperparâmetros
y_pred = best_knn.predict(X_test)

# Avaliar a acurácia do modelo
accuracy = (y_pred == y_test).mean()
print("Acurácia:", accuracy)