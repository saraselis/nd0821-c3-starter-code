"""Training a machine learning model"""

import config
import pandas as pd
import pickle as pkl

from ml import model
from ml.data import process_data
from sklearn.model_selection import train_test_split

# Add code to load in the data.
data = pd.read_csv(config.DATA_PATH)

# Optional enhancement, use K-fold cross validation instead of a
# train-test split.
train, test = train_test_split(data, test_size=config.TEST_SPLIT_SIZE)
X_train, y_train, ecd, lb = process_data(train,
                                         categorical_features=config.cat_feat,
                                         label=config.TARGET,
                                         training=True)

# Proces the test data with the process_data function.
X_test, y_test, _, _ = process_data(test,
                                    categorical_features=config.cat_feat,
                                    label=config.TARGET,
                                    training=False, encoder=ecd, lb=lb)

# Train and save a model.
mod = model.train_model(X_train, y_train)

# Dump the model as a pickle file
with open(config.MODEL_PATH, "wb") as file:
    pkl.dump([ecd, lb, mod], file)

# Inference and evaluation
train_pred = model.inference(mod, X_train)
test_pred = model.inference(mod, X_test)
precision, recall, f_one = model.compute_model_metrics(y_test, test_pred)

print(f"Precision: {precision}\n")
print(f"Recall: {recall}\n")
print(f"F1: {f_one}\n")

model.compute_metrics_by_slice(
    df=test,
    model=mod,
    encoder=ecd,
    lb=lb,
    cat_columns=config.cat_feat,
    target=config.TARGET,
    output_path=config.METRICS_OUTPUT_PATH)
