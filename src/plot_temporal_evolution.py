import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.lines import Line2D

import os
import sys


def import_data(DATA_DIRECTORY, DATE):
    df_path = os.path.join(DATA_DIRECTORY, "posts_groups_" + DATE + ".csv")
    df = pd.read_csv(df_path)
    return df


def clean_data(df):
    df['date'] = pd.to_datetime(df['date']) 
    df['week'] = df['date'].dt.week

    df = df[df['date'] >= "2019-09-15"]
    df = df[df['date'] <= "2020-05-17"]

    df["reaction"] = df[["actual_like_count", "actual_favorite_count", "actual_love_count",
    "actual_wow_count", "actual_haha_count", "actual_sad_count",
    "actual_angry_count", "actual_thankful_count"]].sum(axis=1).astype(int)

    df["interaction"] = df[["reaction", "actual_share_count", "actual_comment_count"]].sum(axis=1).astype(int)
    df["interaction_without_share"] = df[["reaction", "actual_comment_count"]].sum(axis=1).astype(int)
    return df


def plot_interaction_by_day(df):

    plt.figure(figsize=(12, 15))

    for i in range(df['account_name'].nunique()):
        plt.subplot(7, 2, i+1)
        group = df['account_name'].unique()[i]
        
        plt.plot(df[df["account_name"].str.startswith(group)]\
            .groupby(by=["date"])["interaction_without_share"].sum(), label="nombre d'interactions par jour")

        plt.xlim(np.datetime64('2019-09-01'), np.datetime64('2020-05-30'))
        plt.ylim(bottom=0)

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        
        if i < 2:
            plt.legend()

        plt.title(group)


def plot_interaction_by_post(df):

    plt.figure(figsize=(12, 15))

    for i in range(df['account_name'].nunique()):
        group = df['account_name'].unique()[i]

        ax1 = plt.subplot(7, 2, i+1)
        ax2 = ax1.twinx()
        ax2.plot(df[df["account_name"].str.startswith(group)]\
            .groupby(by=["date"])["interaction_without_share"].mean())
        ax2.tick_params(axis='y', labelcolor='#1f77b4')
        ax2.set_ylim(bottom=0)
        
        ax1.plot(df[df["account_name"].str.startswith(group)]\
            ["date"].value_counts().sort_index(), '#d62728')
        ax1.tick_params(axis='y', labelcolor='#d62728')
        ax1.set_ylim(bottom=0)

        if i < 2:
            legend_elements = [Line2D([0], [0], color='#d62728', lw=1, label="nombre de publications par jour"),
                            Line2D([0], [0], color='#1f77b4', lw=1, label="nombre d'interactions par publication")]
            ax2.legend(handles=legend_elements, loc="upper left")

        plt.xlim(np.datetime64('2019-09-01'), np.datetime64('2020-05-30'))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))

        plt.title(group)


def save_graph(FIGURE_DIRECTORY, title, DATE):
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURE_DIRECTORY, title + "_" + DATE + ".png"))
    print("The '{}' graph has been saved in the '{}' folder."
            .format(title, FIGURE_DIRECTORY))


def compute_growth_rate(metric):
    return int(np.round((metric[1] - metric[0]) * 100 / metric[0]))


def print_statistics(df):

    df = df[df["account_name"] != "Wuhan Coronavirus (Latest news, information & discussion)"]
        
    summary_df = pd.DataFrame(columns=(
        'Evolution des interactions par jour',
        'Evolution des publications par jour',
        "Evolution des interactions par publication"
    ))

    for group in df['account_name'].unique():
        interaction = [
            np.sum(df[(df['date'] > "2019-09-15") & (df['date'] <= "2020-01-15") &
                      (df["account_name"]==group)]["interaction_without_share"]),
            np.sum(df[(df['date'] > "2020-01-15") & (df['date'] <= "2020-05-15") &
                      (df["account_name"]==group)]["interaction_without_share"])
        ]
        post = [
            len(df[(df["account_name"]==group) & 
                   (df['date'] > "2019-09-15") & (df['date'] <= "2020-01-15")]),
            len(df[(df["account_name"]==group) & 
                   (df['date'] > "2020-01-15") & (df['date'] <= "2020-05-15")])
        ]
        interaction_per_post = [i/p for i, p in zip(interaction, post)]
        
        summary_df.loc[group] = [
            compute_growth_rate(interaction),
            compute_growth_rate(post),
            compute_growth_rate(interaction_per_post)
        ]

    print(summary_df.sort_values(by='Evolution des interactions par jour', ascending=False).to_string())


if __name__ == "__main__":

    if len(sys.argv) >= 2:
        DATE = sys.argv[1]
    else:
        DATE = "2020_05_19"
        print("The date '{}' has been chosen by default.".format(DATE))

    DATA_DIRECTORY = "data"
    FIGURE_DIRECTORY = "figure"

    df = import_data(DATA_DIRECTORY, DATE)
    df = clean_data(df)

    plot_interaction_by_day(df)
    save_graph(FIGURE_DIRECTORY, "interaction_by_day", DATE)

    plot_interaction_by_post(df)
    save_graph(FIGURE_DIRECTORY, "interaction_by_post", DATE)

    print_statistics(df)


