Intrusion Detection System (IDS)

A Machine Learning-based Intrusion Detection System that detects whether incoming network traffic is safe or anomalous in real time using a trained ML model.
Features: -
1)	Real-time prediction of network anomalies
2)	Uses Decision Tree, KNN, and Logistic Regression for comparison
3)	Frontend built using React.js with a modern dark UI
4)	RESTful Flask API backend for prediction
5)	Feature selection using Random Forest ^) Accuracy and precision comparison of model

Tech Stack: -
1)	Frontend: React.js (MERN Stack)
2)	Backend: Flask (Python)
3)	ML Algorithms: Decision Tree, Logistic Regression, KNN
4)	Dataset:
5)	Other:  Random Forest (for feature selection), scikit-learn, NumPy, Pickle, Pandas


How It Works: -

1)	Trained a model on selected 10 important features from dataset.
2)	Backend receives features from user input via REST API.
3)	Encodes categorical values and passes to the trained model.
4)	Model returns whether the traffic is Normal or Anomalous.

