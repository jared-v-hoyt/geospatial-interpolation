import csv
import pandas as pd


def get_relevant_rows(interpolation_method):
    df_1 = pd.read_csv(
        filepath_or_buffer=f"../data/interpolated_data/{interpolation_method}.csv",
        header=None
    ).rename(columns={2: "third_column"})
    df_2 = pd.read_csv(
        filepath_or_buffer=f"../data/interpolated_data/{interpolation_method}_new.csv",
        header=None
    ).rename(columns={2: "third_column_new"})

    merged_df = df_1.merge(
        right=df_2,
        on=[0, 1],
        how="outer",
        indicator=True
    )
    matching_rows = merged_df[merged_df["_merge"] == "both"]
    matching_rows.to_csv(
        path_or_buf=f"../data/error/{interpolation_method}/matching_rows.csv",
        index=False,
        header=False
    )


def remove_matching_rows(input_csv, output_csv):
    filtered_rows = []

    with open(input_csv, "r") as csvfile:
        csvreader = csv.reader(csvfile)

        for row in csvreader:
            if row[2] != row[3]:
                filtered_rows.append(row)

    with open(output_csv, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(filtered_rows)


if __name__ == "__main__":
    get_relevant_rows("inverse_distance_weighting")
    get_relevant_rows("shape_function")

    base_path = "../data/error/inverse_distance_weighting"
    remove_matching_rows(
        f"{base_path}/matching_rows.csv",
        f"{base_path}/actual_vs_calculated_rows.csv"
    )

    base_path = "../data/error/shape_function"
    remove_matching_rows(
        f"{base_path}/matching_rows.csv",
        f"{base_path}/actual_vs_calculated_rows.csv"
    )