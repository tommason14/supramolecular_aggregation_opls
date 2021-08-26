import re
import pandas as pd
from glob import glob
import seaborn as sns
import matplotlib.pyplot as plt
import sys

def molecules_per_cluster():
    def read(fname):
        cutoff = int(re.match(".*([0-9])-angs", fname).group(1))
        df = []
        with open(fname) as f:
            for line in f.readlines():
                if not line.startswith("#") and not line.startswith("@"):
                    size, proportion = line.split()
                    size = int(size)
                    proportion = float(proportion)
                    df.append([size, proportion])
        df = pd.DataFrame(df, columns=["cluster_size", "proportion"])
        df["cutoff"] = cutoff
        return df

    df = pd.concat(read(f) for f in glob("nvt/analysis/**/histo-clust.xvg"))
    df.to_csv("num_molecules_per_cluster.csv", index=False)
    # cut off 0 and 21
    df["cluster_size"] = pd.Categorical(
        df["cluster_size"], categories=range(1, 21), ordered=True
    )
    df["cutoff"] = pd.Categorical(df["cutoff"], categories=range(3, 7), ordered=True)
    p = sns.barplot(data=df, x="cluster_size", y="proportion", hue="cutoff")
    p.set_xlabel("Cluster size")
    p.set_ylabel("Distribution")
    p.legend(title="Cutoff (Å)", bbox_to_anchor=(0.9, 0.8))
    plt.tight_layout()
    plt.savefig("num_molecules_per_cluster.pdf", dpi=300)
    plt.clf()


def clusters_over_time(rolling_steps=10):
    def read(fname):
        cutoff = int(re.match(".*([0-9])-angs", fname).group(1))
        df = []
        with open(fname) as f:
            for line in f.readlines():
                if not line.startswith("#") and not line.startswith("@"):
                    ps, n = line.split()
                    ps, n = float(ps), int(n)
                    ns = ps / 1000
                    df.append([ns, n])
        df = pd.DataFrame(df, columns=["Time (ns)", "N"])
        df["cutoff"] = cutoff
        return df

    df = pd.concat(read(f) for f in glob("nvt/analysis/**/nclust.xvg"))
    df.to_csv("num_of_clusters_over_time.csv", index=False)
    df["cutoff"] = pd.Categorical(df["cutoff"], categories=range(3, 7), ordered=True)
    df["rolling_N"] = df.groupby("cutoff")["N"].transform(
        lambda col: col.rolling(rolling_steps).mean()
    )
    g = sns.relplot(
        data=df,
        x="Time (ns)",
        y="rolling_N",
        hue="cutoff",
        col="cutoff",
        col_wrap=2,
        kind="line",
        legend=False,
    )
    g.set_titles("{col_name} Å cutoff")
    g.set_axis_labels("Time (ns)", "Number of clusters")
    plt.tight_layout()
    plt.savefig("num_of_clusters_over_time.pdf", dpi=300)
    plt.clf()


def max_number_of_molecules_clustered_over_time(rolling_steps=10):
    def read(fname):
        cutoff = int(re.match(".*([0-9])-angs", fname).group(1))
        df = []
        with open(fname) as f:
            for line in f.readlines():
                if not line.startswith("#") and not line.startswith("@"):
                    ps, n = line.split()
                    ps, n = float(ps), int(n)
                    ns = ps / 1000
                    df.append([ns, n])
        df = pd.DataFrame(df, columns=["Time (ns)", "N"])
        df["cutoff"] = cutoff
        return df

    def rolling_mean(series, **kwargs):
        """
        Plot average of 10 steps
        """
        sns.lineplot(series.rolling(rolling_steps).mean(), ci=None, **kwargs)

    df = pd.concat(read(f) for f in glob("nvt/analysis/**/maxclust.xvg"))
    df.to_csv("max_num_molecules_per_cluster.csv", index=False)
    df["cutoff"] = pd.Categorical(df["cutoff"], categories=range(3, 7), ordered=True)
    df["rolling_N"] = df.groupby("cutoff")["N"].transform(
        lambda col: col.rolling(rolling_steps).mean()
    )
    g = sns.relplot(
        data=df,
        x="Time (ns)",
        y="rolling_N",
        hue="cutoff",
        col="cutoff",
        col_wrap=2,
        kind="line",
        legend=False,
    )
    g.set_titles("{col_name} Å cutoff")
    g.set_axis_labels("Time (ns)", "Number of molecules per cluster")
    plt.tight_layout()
    plt.savefig("max_num_molecules_per_cluster.pdf", dpi=300)
    plt.clf()


def main():
    N = int(sys.argv[1])
    sns.set(style="white", palette="rainbow", font_scale=1.3)
    molecules_per_cluster()
    clusters_over_time(N)
    max_number_of_molecules_clustered_over_time(N)


if __name__ == "__main__":
    main()
