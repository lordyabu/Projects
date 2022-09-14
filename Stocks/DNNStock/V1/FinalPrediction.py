import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow import keras

data_file_path = "Heman hope - Sheet2.csv"

mkt_data = pd.read_csv(data_file_path)

field_names = {'Prediction1', 'Prediction2', 'Prediction3', 'Prediction6', 'Prediction7', 'Prediction8', 'Prediction9',
               'Prediction10'}

f_col_pct1 = tf.feature_column.numeric_column('Prediction1')
f_col_pct2 = tf.feature_column.numeric_column('Prediction2')
f_col_pct3 = tf.feature_column.numeric_column('Prediction3')
f_col_pct4 = tf.feature_column.numeric_column('Prediction6')
f_col_pct5 = tf.feature_column.numeric_column('Prediction7')
f_col_pct6 = tf.feature_column.numeric_column('Prediction8')
f_col_pct7 = tf.feature_column.numeric_column('Prediction9')
f_col_pct8 = tf.feature_column.numeric_column('Prediction10')

feature_cols = [f_col_pct1, f_col_pct2, f_col_pct3, f_col_pct4, f_col_pct5, f_col_pct6, f_col_pct7, f_col_pct8]

x_data = mkt_data.drop('Target', axis=1)
y_data = mkt_data['Target']

x_train = x_data.copy()
y_train = y_data.copy()

input_func = tf.compat.v1.estimator.inputs.pandas_input_fn(x_train, y_train, batch_size=10, num_epochs=100,
                                                                 shuffle=True)
model = tf.estimator.DNNClassifier(hidden_units=[15, 15, 15], feature_columns=feature_cols, n_classes=2)
model.train(input_fn=input_func, steps=100)

all_predictions = []
for i in range(0, 11202):
    da = {'Prediction1': [x_data['Prediction1'][i]], 'Prediction2': [x_data['Prediction2'][i]], 'Prediction3': [x_data['Prediction3'][i]], 'Prediction6': [x_data['Prediction6'][i]],
          'Prediction7': [x_data['Prediction7'][i]], 'Prediction8': [x_data['Prediction8'][i]], 'Prediction9': [x_data['Prediction9'][i]], 'Prediction10': [x_data['Prediction10'][i]]}
    x_p = pd.DataFrame(data=da)
    pred_input_func = tf.compat.v1.estimator.inputs.pandas_input_fn(x=x_p, batch_size=10, num_epochs=1,
                                                                    shuffle=False)
    prediction = model.predict(pred_input_func)
    my_pred = list(prediction)
    pred_val = int(my_pred[0]['classes'][0])
    all_predictions.append(pred_val)
predict_one_dict = {'Prediction': all_predictions}
predict_one_df = pd.DataFrame(predict_one_dict)
predict_one_df.to_csv("TestHemanPredictions.csv")