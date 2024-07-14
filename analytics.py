from collections import Counter

def analyze_performance(tickets):
    total_tickets = len(tickets)
    open_tickets = sum(1 for t in tickets if t['status'] == 'Open')
    closed_tickets = total_tickets - open_tickets
    
    avg_resolution_time = 24  # Placeholder, in a real system you'd calculate this
    
    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "closed_tickets": closed_tickets,
        "average_resolution_time": avg_resolution_time
    }

def predict_common_issues(ticket_descriptions, top_n=3):
    words = [word for desc in ticket_descriptions for word in desc.lower().split()]
    return [word for word, _ in Counter(words).most_common(top_n)]