import pandas as pd
from datetime import datetime
from llm_agent import call_llm
from io import StringIO


def generate_prompt(df):
    today = datetime.today().strftime("%Y-%m-%d")
    csv_text = df.to_csv(index=False)

    prompt = f"""
You are an autonomous AI agent.

Your task is:
- Analyze the attendance check-in log for {today}.
- Assume check-in before 09:10 is Present, between 09:10 and 10:00 is Late, after that or blank is Absent.
- Output the attendance as a table with these columns: Name, Date, Check-in Time, Status

Here is the CSV log:

{csv_text}

Give your output ONLY in CSV format.
"""
    return prompt


def update_sheet(response_csv):
    new_df = pd.read_csv(StringIO(response_csv))

    try:
        existing = pd.read_excel(
            "output/attendance_sheet.xlsx", engine="openpyxl")
        final_df = pd.concat([existing, new_df], ignore_index=True)
    except FileNotFoundError:
        final_df = new_df

    final_df.to_excel("output/attendance_sheet.xlsx", index=False)
    print("[✔] Attendance updated successfully.")


if __name__ == "__main__":
    logs = pd.read_csv("data/logs.csv")
    prompt = generate_prompt(logs)
    result_csv = call_llm(prompt)
    update_sheet(result_csv)
