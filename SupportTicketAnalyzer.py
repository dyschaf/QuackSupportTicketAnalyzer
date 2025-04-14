import json
from datetime import datetime
from dateutil import parser


# diffrent catogorys to loop through to find these key words
categorizes_support_tickets = {
    "login": ["login", "password"],
    "payment": ["payment", "order"],
    "bug": ["missing","bug", "error", "issue","slow response"],
    "feature": ["feature", "request"],

}

# open json file  
def load_tickets(file_path):
   with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data["tickets"]
      
# look for catogorys keywords in support tickets
def get_categorize_support_tickets(support_tickets):
    text = (support_tickets.get("subject", "") + " " + support_tickets.get("description", "")).lower()
    for category, keywords in categorizes_support_tickets.items():
        for word in keywords:
            if word in text:
                return category
    return "not categorized"

# parse date
def parse_date(date_str):
    try:
        return parser.parse(date_str)
    except Exception:
        return None

# Categorizes tickets and returns a count summary plus those created before a cutoff date or with invalid dates.
def analyze_tickets(support_tickets, before_date):
    summary = {}
    old_tickets = []


    for ticket in support_tickets:
        # It categorizes each ticket, counts how many fall into each category,
        category = get_categorize_support_tickets(ticket)
        summary[category] = summary.get(category, 0) + 1


        ticket_date = parse_date(ticket.get("created_at", ""))
        if ticket_date and ticket_date.tzinfo is not None:
            ticket_date = ticket_date.replace(tzinfo=None)

        if ticket_date:
          if ticket_date < before_date:
              old_tickets.append({
                  "id": ticket.get("ticketId", "N/A"),
                  "subject": ticket.get("subject", ""),
                  "date": ticket.get("created_at")
              })
        else:
            old_tickets.append({
                "id": ticket.get("ticketId", "N/A"),
                "subject": ticket.get("subject", ""),
                "date": "date unknown"
            })


    return summary, old_tickets

def main():
    file_path = "support_tickets.json"
# open file
    support_tickets = load_tickets(file_path)
     # Ask user for a cutoff date
    user_input = input("What date would you like the cutoff date (day-month-year) (DD-MM-YYYY): ")
    user_input = user_input.replace("/", "-") 
    try:
        cutoff_date = datetime.strptime(user_input, "%d-%m-%Y")
    except ValueError:
        print("Please write the date in the right format. Use (day - month -year) DD-MM-YYYY.")
        return
    summary, old_tickets = analyze_tickets(support_tickets, cutoff_date)
    
# print summary
    print("\nCategory Summary:")
    for category, count in summary.items():
        print(f"- {category}: {count}")
# old tickes print

    print(f"\nsupport tickets created before cut off date {user_input}:")
    for t in old_tickets:
        subject = t['subject'].strip() if t['subject'].strip() else "subject unknown"
        print(f"- {t['id']}: {subject} ({t['date']})")


            

if __name__ == "__main__":
    main()
