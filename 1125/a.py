from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import pandas as pd
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


df = pd.read_csv('data/iris.csv')

X = df.drop('species', axis = 1) 
y = df['species'] 


X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y 
)


encoder = LabelEncoder()
y_train_encoded = encoder.fit_transform(y_train) 
y_test_encoded = encoder.transform(y_test) 

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


k_list = range(3, 12, 2)
test_accuracies = []

for k in k_list: 
 
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X_train_scaled, y_train_encoded)
    
    
    y_test_pred = model.predict(X_test_scaled)
    
    
    test_acc = accuracy_score(y_test_encoded, y_test_pred)
    test_accuracies.append(test_acc) 


best_k_index = test_accuracies.index(max(test_accuracies))
best_k = k_list[best_k_index]

print("K 값별 Test 정확도 :", test_accuracies)
print(f"최적의 K 값: {best_k}")
print(f"최적 K에서의 Test 정확도: {test_accuracies[best_k_index]:.4f}")


best_model = KNeighborsClassifier(n_neighbors=best_k)
best_model.fit(X_train_scaled, y_train_encoded)


y_test_pred_final = best_model.predict(X_test_scaled)
final_test_acc = accuracy_score(y_test_encoded, y_test_pred_final) 

print(f"최종 모델(최적 K={best_k}) Test 정확도: {final_test_acc:.4f}")


plt.figure(figsize=(8, 5))

plt.plot(k_list,test_accuracies , marker='s', label='Test Accuracy')
plt.xticks(k_list)
plt.xlabel('K (Number of Neighbors)')
plt.ylabel('Accuracy')
plt.title('K 값에 따른 KNN 모델 정확도 변화')
plt.legend()
plt.grid(True)

plt.show()