# -*- coding: utf-8 -*-
"""
Fantrax F1 Perfect Pick V1.1

Imports results from a race weekend
Enumerates all viable driver lineups (within budget cap)
Determines the perfect driver lineup(s), and maximum points that could be 
scored that race weekend
"""
import pandas as pd

# race result csv filename, stored in data subfolder against each race number
race_no = "1"
full_filename = "Data\\" + race_no + ".csv"

# import full csv, strip excess columns, then add Three Letter Indicators
imported_data = pd.read_csv(full_filename)
stripped_data = imported_data[["Player", "Salary", "FPts"]]

tli_dict = {
    "Max Verstappen": "VER",
    "Fernando Alonso": "ALO",
    "Sergio Perez": "PER",
    "Lewis Hamilton": "HAM",
    "Valtteri Bottas": "BOT",
    "Carlos Sainz": "SAI",
    "Pierre Gasly": "GAS",
    "Alexander Albon": "ALB",
    "Lance Stroll": "STR",
    "Kevin Magnussen": "MAG",
    "Nyck de Vries": "DEV",
    "Yuki Tsunoda": "TSU",
    "Logan Sargeant": "SAR",
    "George Russell": "RUS",
    "Daniel Ricciardo": "RIC",
    "Nicholas Latifi": "LAT",
    "Mick Schumacher": "MSC",
    "Felipe Drugovich": "DRU",
    "Zhou Guanyu": "ZHO",
    "Lando Norris": "NOR",
    "Nico Hulkenberg": "HUL",
    "Oscar Piastri": "PIA",
    "Charles Leclerc": "LEC",
    "Esteban Ocon": "OCO",
}

tli_df = pd.DataFrame.from_dict(tli_dict, orient="index", columns=["TLI"])

data = tli_df.join(stripped_data.set_index("Player")).reset_index(
    names="Player"
)

# determine number of drivers to enumerate through
driver_total = len(data)

# create starting counters for best and worst result to be stored in
best_lineup = pd.DataFrame(
    columns=["Lineup", "Total Sal", "Individual Pts", "Total Pts"]
)
best_score = 0
worst_lineup = pd.DataFrame(
    columns=["Lineup", "Total Sal", "Individual Pts", "Total Pts"]
)
worst_score = 0


# generate all viable driver lineup combinations
# driver lineups must be in descending table order
# this prevents unnecessary re-evaluating combinations
for d_1 in range((driver_total - 5)):
    d_1_sal = data.at[d_1, "Salary"]
    d_1_tli = data.at[d_1, "TLI"]
    d_1_pts = data.at[d_1, "FPts"]
    for d_2 in range((d_1 + 1), (driver_total - 4)):
        d_2_sal = data.at[d_2, "Salary"]
        d_2_tli = data.at[d_2, "TLI"]
        d_2_pts = data.at[d_2, "FPts"]
        for d_3 in range((d_2 + 1), (driver_total - 3)):
            d_3_sal = data.at[d_3, "Salary"]
            d_3_tli = data.at[d_3, "TLI"]
            d_3_pts = data.at[d_3, "FPts"]
            for d_4 in range((d_3 + 1), (driver_total - 2)):
                d_4_sal = data.at[d_4, "Salary"]
                d_4_tli = data.at[d_4, "TLI"]
                d_4_pts = data.at[d_4, "FPts"]
                for d_5 in range((d_4 + 1), (driver_total - 1)):
                    d_5_sal = data.at[d_5, "Salary"]
                    d_5_tli = data.at[d_5, "TLI"]
                    d_5_pts = data.at[d_5, "FPts"]
                    for d_6 in range((d_5 + 1), driver_total):
                        d_6_sal = data.at[d_6, "Salary"]
                        d_6_tli = data.at[d_6, "TLI"]
                        d_6_pts = data.at[d_6, "FPts"]

                        # calculate total salary of lineup
                        total_sal = (
                            d_1_sal
                            + d_2_sal
                            + d_3_sal
                            + d_4_sal
                            + d_5_sal
                            + d_6_sal
                        )

                        # if meets salary limit, calculate points
                        if total_sal <= 100:

                            # calculate total points
                            total_pts = (
                                d_1_pts
                                + d_2_pts
                                + d_3_pts
                                + d_4_pts
                                + d_5_pts
                                + d_6_pts
                            )

                            # store if matches or beats current best total
                            if (total_pts >= best_score) or (
                                total_pts <= worst_score
                            ):

                                # list lineup
                                lineup = str(
                                    [
                                        d_1_tli,
                                        d_2_tli,
                                        d_3_tli,
                                        d_4_tli,
                                        d_5_tli,
                                        d_6_tli,
                                    ]
                                )

                                # list individual points
                                indiv_pts = str(
                                    [
                                        d_1_pts,
                                        d_2_pts,
                                        d_3_pts,
                                        d_4_pts,
                                        d_5_pts,
                                        d_6_pts,
                                    ]
                                )

                                # prepare result
                                result = {
                                    "Lineup": lineup,
                                    "Total Sal": total_sal,
                                    "Individual Pts": indiv_pts,
                                    "Total Pts": total_pts,
                                }
                                result_df = pd.DataFrame(
                                    data=result, index=[0]
                                )
                                # if matches best score, append result
                                if total_pts == best_score:
                                    best_lineup = pd.concat(
                                        [best_lineup, result_df],
                                        ignore_index=True,
                                    )

                                # if beats best score, reset table and record
                                if total_pts > best_score:
                                    best_lineup = pd.DataFrame(
                                        columns=[
                                            "Lineup",
                                            "Total Sal",
                                            "Individual Pts",
                                            "Total Pts",
                                        ]
                                    )
                                    best_lineup = pd.concat(
                                        [best_lineup, result_df],
                                        ignore_index=True,
                                    )
                                    best_score = total_pts

                                # if matches worst score, append result
                                if total_pts == worst_score:
                                    worst_lineup = pd.concat(
                                        [worst_lineup, result_df],
                                        ignore_index=True,
                                    )

                                # if new worst score, reset table and record
                                if total_pts < worst_score:
                                    worst_lineup = pd.DataFrame(
                                        columns=[
                                            "Lineup",
                                            "Total Sal",
                                            "Individual Pts",
                                            "Total Pts",
                                        ]
                                    )
                                    worst_lineup = pd.concat(
                                        [worst_lineup, result_df],
                                        ignore_index=True,
                                    )
                                    worst_score = total_pts
print("Best lineup:")
print(best_lineup)
print("Worst lineup:")
print(worst_lineup)
# total combinations assessed: 63661
