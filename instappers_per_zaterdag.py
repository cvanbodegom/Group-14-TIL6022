import csv
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    csv_path = (
        Path.cwd()
        / "Gefilterde datasets"
        / "Instappers_per_uur_export_V3_2024.csv"
    )
    if not csv_path.is_file():
        raise FileNotFoundError(
            f"CSV niet gevonden: {csv_path}. "
            "Voer de code uit vanuit de projectmap of controleer het bestandspad."
        )
    # The file has unmatched quotes around its header and final value.
    df = pd.read_csv(
        csv_path,
        skiprows=1,
        names=["Datum", "Uur", "Aantal_check_ins"],
        quoting=csv.QUOTE_NONE,
    )
    df["Datum"] = pd.to_datetime(df["Datum"], format="%d-%m-%Y")
    df["Uur"] = pd.to_numeric(df["Uur"])
    df["Aantal_check_ins"] = pd.to_numeric(
        df["Aantal_check_ins"].astype(str).str.strip('"')
    )

    # Sum the hourly counts for each Saturday; each bar represents one week.
    saturdays = df.loc[df["Datum"].dt.dayofweek == 5].copy()
    saturday_totals = saturdays.groupby("Datum")["Aantal_check_ins"].sum().sort_index()
    koningsdag = pd.Timestamp("2024-04-27")
    if koningsdag not in saturday_totals.index:
        raise ValueError("Koningsdag 2024 ontbreekt in de dataset.")

    blue = "#2878B5"
    orange = "#F28E2B"
    other_saturday_mean = saturday_totals.drop(koningsdag).mean()
    koningsdag_total = saturday_totals.loc[koningsdag]
    percent_above_mean = (koningsdag_total / other_saturday_mean - 1) * 100
    rank = int(saturday_totals.rank(ascending=False, method="min").loc[koningsdag])

    # Compare King's Day by hour with the other Saturdays in April.
    april_other_saturdays = saturdays.loc[
        saturdays["Datum"].dt.month.eq(4) & saturdays["Datum"].ne(koningsdag)
    ]
    april_hourly_mean = april_other_saturdays.groupby("Uur")[
        "Aantal_check_ins"
    ].mean()
    koningsdag_hourly = (
        saturdays.loc[saturdays["Datum"].eq(koningsdag)]
        .set_index("Uur")["Aantal_check_ins"]
        .sort_index()
    )

    fig, (ax_weekly, ax_hourly) = plt.subplots(
        1, 2, figsize=(17, 6.5), gridspec_kw={"width_ratios": [1.35, 1]}
    )
    fig.suptitle(
        "Instappers op zaterdagen in 2024",
        fontsize=19,
        fontweight="bold",
        y=1.03,
    )

    # Left: all Saturday totals across the year, with King's Day highlighted.
    bar_colors = [orange if date == koningsdag else blue for date in saturday_totals.index]
    ax_weekly.bar(
        saturday_totals.index,
        saturday_totals.values,
        color=bar_colors,
        width=5.5,
        zorder=3,
    )
    ax_weekly.axhline(
        other_saturday_mean,
        color=blue,
        linestyle="--",
        linewidth=1.8,
        label=f"Gemiddelde overige zaterdagen: {other_saturday_mean:,.0f}",
    )
    ax_weekly.annotate(
        f"27 april (Koningsdag)\n{koningsdag_total:,.0f} instappers"
        f"\n{percent_above_mean:.0f}% boven gemiddelde\n#{rank} drukste zaterdag",
        xy=(koningsdag, koningsdag_total),
        xytext=(koningsdag + pd.Timedelta(days=28), koningsdag_total * 1.08),
        color=orange,
        fontweight="bold",
        arrowprops={"arrowstyle": "->", "color": orange, "lw": 1.8},
        ha="left",
        va="bottom",
    )
    ax_weekly.set_title("Totaal per zaterdag (elke staaf = een week)", fontsize=13)
    ax_weekly.set_ylabel("Aantal instappers")
    ax_weekly.set_xlabel("Datum in 2024")
    ax_weekly.set_xticks(saturday_totals.index[::4])
    ax_weekly.set_xticklabels(
        [date.strftime("%d %b") for date in saturday_totals.index[::4]],
        rotation=40,
        ha="right",
    )
    ax_weekly.set_ylim(0, saturday_totals.max() * 1.3)
    ax_weekly.grid(axis="y", alpha=0.2, zorder=0)
    ax_weekly.legend(frameon=False, loc="upper left")

    # Right: compare the hourly pattern to see when King's Day was busier.
    ax_hourly.plot(
        april_hourly_mean.index,
        april_hourly_mean.values,
        color=blue,
        marker="o",
        linewidth=2.5,
        markersize=5,
        label="Gemiddelde andere zaterdagen in april",
    )
    ax_hourly.plot(
        koningsdag_hourly.index,
        koningsdag_hourly.values,
        color=orange,
        marker="o",
        linewidth=2.8,
        markersize=5,
        label="27 april (Koningsdag)",
    )
    ax_hourly.set_title(
        "Instappers per uur: 27 april vs. andere aprilzaterdagen", fontsize=13
    )
    ax_hourly.set_xlabel("Uur van de dag")
    ax_hourly.set_ylabel("Gemiddeld aantal instappers per uur")
    ax_hourly.set_xticks(range(0, 24, 2))
    ax_hourly.grid(axis="y", alpha=0.2)
    ax_hourly.legend(frameon=False, loc="upper left")

    fig.tight_layout()
    plt.show()

    print(
        f"Zaterdagen in de dataset: {len(saturday_totals)} | "
        f"27 april: {koningsdag_total:,.1f} instappers | "
        f"gemiddelde overige zaterdagen: {other_saturday_mean:,.1f} | "
        f"verschil: +{percent_above_mean:.1f}% | "
        f"rang: {rank} van {len(saturday_totals)}"
    )


if __name__ == "__main__":
    main()
