import sys
import pandas as pd

def main():
    stripe_export = "unified_payments.csv"
    stripe_data = pd.read_csv(stripe_export)
    for competition in get_competitions(stripe_data):
        registration_fees = sum_registration_fees(stripe_data, competition)
        refunds = sum_refunds(stripe_data, competition)
        stripe_fees = sum_competition_stripe_fees(stripe_data, competition)
        print(competition)
        print(f"Registration fees: {registration_fees}")
        print(f"Refunds: {refunds}")
        print(f"Stripe fees: {stripe_fees}\n")
        print(f"Total income: {registration_fees - refunds - stripe_fees}")

def sum_registration_fees(stripe_data, competition_name: str) -> float:
    filtered_data = stripe_data[stripe_data["competition (metadata)"] == competition_name]
    filtered_data = filtered_data[filtered_data["Status"] == "Paid"]
    return round(sum(float(i.replace(",", ".")) for i in filtered_data["Converted Amount"].dropna().values), 2)

def sum_competition_stripe_fees(stripe_data, competition_name) -> float:
    filtered_data = stripe_data[stripe_data["competition (metadata)"] == competition_name]
    stripe_fees = round(sum(float(i.replace(",", ".")) for i in filtered_data["Fee"].dropna().values), 2)
    return stripe_fees

def sum_refunds(stripe_data, competition_name: str) -> float:
    filtered_data = stripe_data[stripe_data["competition (metadata)"] == competition_name]
    return round(sum(float(i.replace(",", ".")) for i in filtered_data["Converted Amount Refunded"].dropna().values), 2)

def sum_invoices(stripe_data) -> float:
    filtered_data = stripe_data[stripe_data["competition (metadata)"].fillna(0) == 0]
    filtered_data = filtered_data[filtered_data["Status"] != "Failed"]
    return round(sum(float(i.replace(",", ".")) for i in filtered_data["Converted Amount"].dropna().values), 2)

def sum_invoce_fees(stripe_data) -> float:
    filtered_data = stripe_data[stripe_data["competition (metadata)"].fillna(0) == 0]
    stripe_fees = round(sum(float(i.replace(",", ".")) for i in filtered_data["Fee"].dropna().values), 2)
    return stripe_fees

def get_competitions(stripe_data) -> list[str]:
    return list(set(stripe_data["competition (metadata)"].dropna()))

def sum_total_income(stripe_data) -> float:
    filtered_data = stripe_data[stripe_data["Status"] == "Paid"]
    return round(sum(float(i.replace(",", ".")) for i in filtered_data["Converted Amount"].dropna().values), 2)

def sum_total_refunds(stripe_data) -> float:
    return round(sum(float(i.replace(",", ".")) for i in stripe_data["Converted Amount Refunded"].dropna().values), 2)

def sum_stripe_fees(stripe_data) -> float:
    return round(sum(float(i.replace(",", ".")) for i in stripe_data["Fee"].dropna().values), 2)

def sum_unmarked_refunds(stripe_data) -> float:
    filtered_data = stripe_data[stripe_data["competition (metadata)"].fillna(0) == 0]
    return round(sum(float(i.replace(",", ".")) for i in filtered_data["Converted Amount Refunded"].dropna().values), 2)

def get_dates(stripe_data) -> list[str]:
    dates = stripe_data["Created date (UTC)"].dropna().values
    dates = [i.split(" ")[0] for i in dates]
    return list(set(dates))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f'error: missing argument, input file')
        exit(1)
    stripe_export = sys.argv[1]
    main()
