import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow import keras


def predict_all(start, end, num_features):
    hundred_predictions = []
    for i in range(start, end):
        if num_features == 1:
            da = {'1P': [x_data['1P'][i]]}
        elif num_features == 2:
            da = {'1P': [x_data['1P'][i]], '2P': [x_data['2P'][i]]}
        elif num_features == 3:
            da = {'1P': [x_data['1P'][i]], '2P': [x_data['2P'][i]], '3P': [x_data['3P'][i]]}
        elif num_features == 4:
            da = {'1P': [x_data['1P'][i]], '2P': [x_data['2P'][i]], '3P': [x_data['3P'][i]], '4P': [x_data['4P'][i]]}
        elif num_features == 5:
            da = {'1P': [x_data['1P'][i]], '2P': [x_data['2P'][i]], '3P': [x_data['3P'][i]], '4P': [x_data['4P'][i]],
                  '5P': [x_data['5P'][i]]}
        elif num_features == 6:
            da = {'1P': [x_data['1P'][i]], '2P': [x_data['2P'][i]], '3P': [x_data['3P'][i]], '4P': [x_data['4P'][i]],
                  '5P': [x_data['5P'][i]], '6P': [x_data['6P'][i]]}
        elif num_features == 7:
            da = {'1P': [x_data['1P'][i]], '2P': [x_data['2P'][i]], '3P': [x_data['3P'][i]], '4P': [x_data['4P'][i]],
                  '5P': [x_data['5P'][i]], '6P': [x_data['6P'][i]], '7P': [x_data['7P'][i]]}
        elif num_features == 8:
            da = {'1P': [x_data['1P'][i]], '2P': [x_data['2P'][i]], '3P': [x_data['3P'][i]], '4P': [x_data['4P'][i]],
                  '5P': [x_data['5P'][i]], '6P': [x_data['6P'][i]], '7P': [x_data['7P'][i]], '8P': [x_data['8P'][i]]}
        elif num_features == 9:
            da = {'1P': [x_data['1P'][i]], '2P': [x_data['2P'][i]], '3P': [x_data['3P'][i]], '4P': [x_data['4P'][i]],
                  '5P': [x_data['5P'][i]], '6P': [x_data['6P'][i]], '7P': [x_data['7P'][i]], '8P': [x_data['8P'][i]],
                  '9P': [x_data['9P'][i]]}
        elif num_features == 10:
            da = {'1P': [x_data['1P'][i]], '2P': [x_data['2P'][i]], '3P': [x_data['3P'][i]], '4P': [x_data['4P'][i]],
                  '5P': [x_data['5P'][i]], '6P': [x_data['6P'][i]], '7P': [x_data['7P'][i]], '8P': [x_data['8P'][i]],
                  '9P': [x_data['9P'][i]], '10P': [x_data['10P'][i]]}
        x_p = pd.DataFrame(data=da)
        pred_input_func = tf.compat.v1.estimator.inputs.pandas_input_fn(x=x_p, batch_size=10, num_epochs=1,
                                                                        shuffle=False)
        prediction = model.predict(pred_input_func)
        my_pred = list(prediction)
        pred_val = int(my_pred[0]['classes'][0])
        hundred_predictions.append(pred_val)

    return hundred_predictions


data_file_path = "V0.062 Townsend Data - Sheet1.csv"

mkt_data = pd.read_csv(data_file_path)

mkt_data["Target"] = mkt_data.rolling(2).apply(lambda x: x.iloc[1] > x.iloc[0])["Close"]
for i in range(0, 11202):
  if mkt_data["Close"][i] / mkt_data["1"][i] > 1.0011:
    mkt_data.loc[i, 'Target'] = 1
  else:
    mkt_data.loc[i, 'Target'] = 0

field_names = {'1P', '2P', '3P', '4P', '5P', '6P', '7P', '8P', '9P', '10P'}

f_col_pct1 = tf.feature_column.numeric_column('1P')
f_col_pct2 = tf.feature_column.numeric_column('2P')
f_col_pct3 = tf.feature_column.numeric_column('3P')
f_col_pct4 = tf.feature_column.numeric_column('4P')
f_col_pct5 = tf.feature_column.numeric_column('5P')
f_col_pct6 = tf.feature_column.numeric_column('6P')
f_col_pct7 = tf.feature_column.numeric_column('7P')
f_col_pct8 = tf.feature_column.numeric_column('8P')
f_col_pct9 = tf.feature_column.numeric_column('9P')
f_col_pct10 = tf.feature_column.numeric_column('10P')

feature_cols_full = [f_col_pct1, f_col_pct2, f_col_pct3, f_col_pct4, f_col_pct5, f_col_pct6, f_col_pct7, f_col_pct8, f_col_pct9, f_col_pct10]
feature_cols = [f_col_pct1]

x_data = mkt_data.drop(['Close', '1', '2', '3','4', '5', '6', '7', '8', '9', '10', '11', 'Target'], axis=1)
y_data = mkt_data['Target']

# 1 features
feature_cols = [f_col_pct1]

x_train = x_data.copy()
y_train = y_data.copy()

input_func = tf.compat.v1.estimator.inputs.pandas_input_fn(x_train, y_train, batch_size=10, num_epochs=100,
                                                                 shuffle=True)
model = tf.estimator.DNNClassifier(hidden_units=[15, 15, 15], feature_columns=feature_cols, n_classes=2)
model.train(input_fn=input_func, steps=100)

predict_one = predict_all(0, 11202, 1)
predict_one_dict = {'Prediction': predict_one}
predict_one_df = pd.DataFrame(predict_one_dict)
predict_one_df.to_csv("predictions_one_feature1.csv")

# 2 Features
feature_cols = [f_col_pct1, f_col_pct2]

x_train = x_data.copy()
y_train = y_data.copy()

input_func = tf.compat.v1.estimator.inputs.pandas_input_fn(x_train, y_train, batch_size=10, num_epochs=100,
                                                                 shuffle=True)
model = tf.estimator.DNNClassifier(hidden_units=[15, 15, 15], feature_columns=feature_cols, n_classes=2)
model.train(input_fn=input_func, steps=100)

predict_two = predict_all(0, 11202, 2)
predict_two_dict = {'Prediction': predict_two}
predict_two_df = pd.DataFrame(predict_two_dict)
predict_two_df.to_csv("predictions_two_feature1.csv")


# 3 Features
feature_cols = [f_col_pct1, f_col_pct2, f_col_pct3]

x_train = x_data.copy()
y_train = y_data.copy()

input_func = tf.compat.v1.estimator.inputs.pandas_input_fn(x_train, y_train, batch_size=10, num_epochs=100,
                                                                 shuffle=True)
model = tf.estimator.DNNClassifier(hidden_units=[15, 15, 15], feature_columns=feature_cols, n_classes=2)
model.train(input_fn=input_func, steps=100)

predict_three = predict_all(0, 11202, 3)
predict_three_dict = {'Prediction': predict_three}
predict_three_df = pd.DataFrame(predict_three_dict)
predict_three_df.to_csv("predictions_three_feature1.csv")

# 4 Features
feature_cols = [f_col_pct1, f_col_pct2, f_col_pct3, f_col_pct4]

x_train = x_data.copy()
y_train = y_data.copy()

input_func = tf.compat.v1.estimator.inputs.pandas_input_fn(x_train, y_train, batch_size=10, num_epochs=100,
                                                                 shuffle=True)
model = tf.estimator.DNNClassifier(hidden_units=[15, 15, 15], feature_columns=feature_cols, n_classes=2)
model.train(input_fn=input_func, steps=100)

predict_four = predict_all(0, 11202, 4)
predict_four_dict = {'Prediction': predict_four}
predict_four_df = pd.DataFrame(predict_four_dict)
predict_four_df.to_csv("predictions_four_feature1.csv")

# 5 Features
feature_cols = [f_col_pct1, f_col_pct2, f_col_pct3, f_col_pct4, f_col_pct5]

x_train = x_data.copy()
y_train = y_data.copy()

input_func = tf.compat.v1.estimator.inputs.pandas_input_fn(x_train, y_train, batch_size=10, num_epochs=100,
                                                                 shuffle=True)
model = tf.estimator.DNNClassifier(hidden_units=[15, 15, 15], feature_columns=feature_cols, n_classes=2)
model.train(input_fn=input_func, steps=100)

predict_five = predict_all(0, 11202, 5)
predict_five_dict = {'Prediction': predict_five}
predict_five_df = pd.DataFrame(predict_five_dict)
predict_five_df.to_csv("predictions_five_feature1.csv")

# 6 Features
feature_cols = [f_col_pct1, f_col_pct2, f_col_pct3, f_col_pct4, f_col_pct5, f_col_pct6]

x_train = x_data.copy()
y_train = y_data.copy()

input_func = tf.compat.v1.estimator.inputs.pandas_input_fn(x_train, y_train, batch_size=10, num_epochs=100,
                                                                 shuffle=True)
model = tf.estimator.DNNClassifier(hidden_units=[15, 15, 15], feature_columns=feature_cols, n_classes=2)
model.train(input_fn=input_func, steps=100)

predict_six = predict_all(0, 11202, 6)
predict_six_dict = {'Prediction': predict_six}
predict_six_df = pd.DataFrame(predict_six_dict)
predict_six_df.to_csv("predictions_six_feature1.csv")

# 7 Features
feature_cols = [f_col_pct1, f_col_pct2, f_col_pct3, f_col_pct4, f_col_pct5, f_col_pct6, f_col_pct7]

x_train = x_data.copy()
y_train = y_data.copy()

input_func = tf.compat.v1.estimator.inputs.pandas_input_fn(x_train, y_train, batch_size=10, num_epochs=100,
                                                                 shuffle=True)
model = tf.estimator.DNNClassifier(hidden_units=[15, 15, 15], feature_columns=feature_cols, n_classes=2)
model.train(input_fn=input_func, steps=100)

predict_seven = predict_all(0, 11202, 7)
predict_seven_dict = {'Prediction': predict_seven}
predict_seven_df = pd.DataFrame(predict_seven_dict)
predict_seven_df.to_csv("predictions_seven_feature1.csv")

# 8 Features
feature_cols = [f_col_pct1, f_col_pct2, f_col_pct3, f_col_pct4, f_col_pct5, f_col_pct6, f_col_pct7, f_col_pct8]

x_train = x_data.copy()
y_train = y_data.copy()

input_func = tf.compat.v1.estimator.inputs.pandas_input_fn(x_train, y_train, batch_size=10, num_epochs=100,
                                                                 shuffle=True)
model = tf.estimator.DNNClassifier(hidden_units=[15, 15, 15], feature_columns=feature_cols, n_classes=2)
model.train(input_fn=input_func, steps=100)

predict_eight = predict_all(0, 11202, 8)
predict_eight_dict = {'Prediction': predict_eight}
predict_eight_df = pd.DataFrame(predict_eight_dict)
predict_eight_df.to_csv("predictions_eight_feature1.csv")

# 9 Features
feature_cols = [f_col_pct1, f_col_pct2, f_col_pct3, f_col_pct4, f_col_pct5, f_col_pct6, f_col_pct7, f_col_pct8, f_col_pct9]

x_train = x_data.copy()
y_train = y_data.copy()

input_func = tf.compat.v1.estimator.inputs.pandas_input_fn(x_train, y_train, batch_size=10, num_epochs=100,
                                                                 shuffle=True)
model = tf.estimator.DNNClassifier(hidden_units=[15, 15, 15], feature_columns=feature_cols, n_classes=2)
model.train(input_fn=input_func, steps=100)

predict_nine = predict_all(0, 11202, 9)
predict_nine_dict = {'Prediction': predict_nine}
predict_nine_df = pd.DataFrame(predict_nine_dict)
predict_nine_df.to_csv("predictions_nine_feature1.csv")

# 10 Features
feature_cols = [f_col_pct1, f_col_pct2, f_col_pct3, f_col_pct4, f_col_pct5, f_col_pct6, f_col_pct7, f_col_pct8, f_col_pct9, f_col_pct10]

x_train = x_data.copy()
y_train = y_data.copy()

input_func = tf.compat.v1.estimator.inputs.pandas_input_fn(x_train, y_train, batch_size=10, num_epochs=100,
                                                                 shuffle=True)
model = tf.estimator.DNNClassifier(hidden_units=[15, 15, 15], feature_columns=feature_cols, n_classes=2)
model.train(input_fn=input_func, steps=100)

predict_ten = predict_all(0, 11202, 10)
predict_ten_dict = {'Prediction': predict_ten}
predict_ten_df = pd.DataFrame(predict_ten_dict)
predict_ten_df.to_csv("predictions_ten_feature1.csv")





