import glob
import pandas as pd


def transform_df_to_context_df(df, context_window=7):
    list_of_contexts = []
    for i in range(context_window, len(df['text'])):
        row = []
        prev = i - 1 - context_window  # responce and 7 previous responces
        for j in range(i, prev, -1):
            row.append(df['text'][j])
        list_of_contexts.append(row)
    columns = ['response', 'context']
    columns = columns + ['context/'+str(i) for i in range(context_window-1)]
    return pd.DataFrame.from_records(list_of_contexts, columns=columns)


def get_output_df(path):
    """ Create dataset that will be used as training data:
    each phrase and previous 7 as a context window are a training object.
    """
    df = pd.read_csv(path)
    df = df.dropna().reset_index(drop=True)
    df_output = []
    if 'page_number' in df.columns:
        for page in set(df['page_number']):
            df_page = df[df['page_number'] == page].reset_index(drop=True)
            df_output.append(transform_df_to_context_df(df_page))
    else:
        df_output.append(transform_df_to_context_df(df))
    return pd.DataFrame(pd.concat(df_output))


def preprocess_all_files(paths_list):
    preprocessed_files = []
    for path in paths_list:
        preprocessed_files.append(get_output_df(path))
    return pd.DataFrame(pd.concat(preprocessed_files))

# Get documents and transform to one dataframe
data_path = "data/*.csv"
files_with_data = [file for file in glob.glob(data_path)]
df_overall = preprocess_all_files(files_with_data)
df_overall.to_csv("data/data_preprocessed.csv", index=False)
