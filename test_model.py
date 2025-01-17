import pytest
import pandas as pd
import sys
from sklearn.model_selection import train_test_split


try:
    import starter.config as config
    from starter.ml.data import process_data
    from starter.ml.model import (train_model, inference,
                                  compute_model_metrics)
except ModuleNotFoundError:
    sys.path.append('./')
    import starter.config as config
    from starter.ml.data import process_data
    from starter.ml.model import (train_model, inference,
                                  compute_model_metrics)


@pytest.fixture()
def input_df():
    """Test the input dataframe and split

    Returns:
        pandas df: train and test dataset
    """
    df = pd.read_csv(config.DATA_PATH)
    train, test = train_test_split(df, test_size=config.TEST_SPLIT_SIZE)
    return train, test


def test_inference(input_df):
    """Test the inference

    Args:
        input_df (np.array): predictions
    """
    train_df, _ = input_df

    X_train, y_train, _, _ = process_data(
        X=train_df,
        categorical_features=config.cat_feat,
        label=config.TARGET,
        training=True
    )

    clf = train_model(X_train, y_train)
    preds = inference(clf, X_train)

    assert len(preds) == len(X_train)


def test_process_data(input_df):
    """input dataframe

    Args:
        input_df (np.array): train and test dataframe
    """

    train_df, test_df = input_df

    X_train, y_train, _, _ = process_data(
        X=train_df,
        categorical_features=config.cat_feat,
        label=config.TARGET,
        training=True
    )

    X_test, y_test, _, _ = process_data(
        X=test_df,
        categorical_features=config.cat_feat,
        label=config.TARGET,
        training=True,

    )

    assert len(X_train) == len(y_train)
    assert len(X_test) == len(y_test)


def test_compute_metrics(input_df):
    """_summary_

    Args:
        input_df (pandas df): testing comuting metrics.
    """
    train, _ = input_df

    X_train, y_train, encoder, lb = process_data(
        X=train,
        categorical_features=config.cat_feat,
        label=config.TARGET,
        training=True
    )

    clf = train_model(X_train, y_train)
    preds = inference(clf, X_train)

    precision, recall, f_one = compute_model_metrics(y_train, preds)

    for metric in [precision, recall, f_one]:
        assert metric <= 1.0
