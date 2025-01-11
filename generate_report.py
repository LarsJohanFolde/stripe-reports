import sys
from stripe_sorter import *
from fpdf import FPDF


unmarked_transfers = "NKF Dues"
stripe_export = "payments.csv"
stripe_data = pd.read_csv(stripe_export)
output_file = f"report"
width = 0
height = 5
font = "courier"

class PDF(FPDF):
    def header(self):
        title = f"NKF Stripe Report"
        self.image("./assets/logo.png", 10, 8, 25)
        self.set_font(font, "B", 16)
        self.cell(0, 10, title, ln=True, align="C")
        self.set_font(font, "B", 11)
        self.cell(0, 5, f"({min(get_dates(stripe_data))} - {max(get_dates(stripe_data))})", align="C")
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font(font, "I", 8)
        self.set_font(font, "I", 10)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C", center=True)

def main() -> None:
    pdf = PDF("P", "mm", "A4")

    pdf.add_page()
    pdf.set_font(font)


    # Per-competition data
    pdf.set_font(style="B")
    # Headers
    pdf.cell(width, height, "Competition Name", border=True, ln=False)
    pdf.cell(width, height, "Registration Fees", center=True, align="C")
    pdf.cell(width, height, "Refunds", align="C")
    pdf.cell(width, height, "Stripe Fees", align="R", ln=True)
    # Data per competition
    pdf.set_font(font, "", 11)
    for competition in get_competitions(stripe_data):
        pdf.cell(width, height, competition, border=True, ln=False)
        pdf.set_text_color(0, 153, 0)
        pdf.cell(width, height, f"{sum_registration_fees(stripe_data, competition)}", center=True, align="C")
        pdf.set_text_color(204, 0, 0)
        if sum_refunds(stripe_data, competition):
            pdf.cell(width, height, f"{-sum_refunds(stripe_data, competition)}", align="C")
        pdf.cell(width, height, f"{-sum_competition_stripe_fees(stripe_data, competition)}", align="R")
        pdf.set_text_color(0, 0, 0)
        pdf.cell(width, 5, ln=True)

    pdf.cell(width, height, "", ln=True)

    # NKF Dues
    pdf.set_font(style="B")
    # Headers
    pdf.cell(width, height, unmarked_transfers, border=True, ln=False)
    pdf.cell(width, height, "Income", center=True, align="C")
    if sum_unmarked_refunds(stripe_data):
        pdf.cell(width, height, "Refunds", align="C")
    pdf.cell(width, height, "Stripe Fees", align="R", ln=True)
    # Data
    pdf.set_font(style="")
    pdf.cell(width, height, "", border=True, ln=False)
    pdf.set_text_color(0, 153, 0)
    pdf.cell(width, height, f"{sum_invoices(stripe_data)}", center=True, align="C")
    pdf.set_text_color(204, 0, 0)
    if sum_unmarked_refunds(stripe_data):
        pdf.cell(width, height, f"{-sum_unmarked_refunds(stripe_data)}", align="C")
    pdf.cell(width, height, f"{-sum_invoce_fees(stripe_data)}", align="R", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(width, 5, ln=True)

    pdf.cell(width, height, "", ln=True)
    pdf.cell(width, height, "", ln=True)

    # Totals
    pdf.set_font(style="B")
    pdf.cell(width, height, "Totals", border=True, center=True, align="C", ln=True)

    pdf.cell(width, height, "Total Income", border=True, ln=False)
    pdf.cell(width, height, "Total Refunds", center=True, align="C")
    pdf.cell(width, height, "Total Stripe Fees", align="R", ln=True)
    pdf.set_font(style="")
    pdf.set_text_color(0, 153, 0)
    pdf.cell(width, height, f"{sum_total_income(stripe_data)}", border=True)
    pdf.set_text_color(204, 0, 0)
    pdf.cell(width, height, f"{-sum_total_refunds(stripe_data)}", center=True, align="C")
    pdf.cell(width, height, f"{-sum_stripe_fees(stripe_data)}", align="R")
    pdf.set_text_color(0, 0, 0)

    pdf.output(f"{output_file}.pdf")
    print(f'file saved as {output_file}.pdf')

if __name__ == '__main__': 
    if len(sys.argv) < 2:
        print(f'error: missing argument, input file')
        exit(1)
    stripe_export = sys.argv[1]
    main()
