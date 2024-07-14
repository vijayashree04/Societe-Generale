import csv
from knowledge_base import KnowledgeBase
from analytics import analyze_performance, predict_common_issues
import random
from sklearn.pipeline import Pipeline
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

class ServiceDesk:
    def __init__(self):
        self.classifier = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', MultinomialNB())
        ])
        self.knowledge_base = KnowledgeBase()
        self.tickets = []
        self.agent_skills = {
            "Agent1": ["Network", "Hardware"],
            "Agent2": ["Account", "Software"],
            "Agent3": ["Email", "Software"]
        }

        self.csv_filename = 'tickets.csv'
        self.load_tickets_from_csv()

    def train_classifier(self):
        # Load actual training data here
        training_data = [
            ("network issue", "Network"),
            ("password reset", "Account"),
            ("software bug", "Software"),
            ("printer not working", "Hardware"),
            ("email configuration", "Email")
        ]
        X = [d[0] for d in training_data]
        y = [d[1] for d in training_data]
        self.classifier.fit(X, y)
        
        # Save the trained model
        joblib.dump(self.classifier, 'service_desk_classifier.joblib')

    def load_classifier(self):
        # Load the trained model
        self.classifier = joblib.load('service_desk_classifier.joblib')

    def predict(self, user_input):
        if not user_input or not isinstance(user_input, str):
            raise ValueError("Input must be a non-empty string")
        
        try:
            prediction = self.classifier.predict([user_input])
            return prediction[0] if isinstance(prediction, (list, np.ndarray)) else prediction
        except AttributeError:
            raise AttributeError("Classifier object does not have a 'predict' method")
        except Exception as e:
            raise RuntimeError(f"Prediction failed: {str(e)}")

    def handle_user_query(self, user_input):
        category = self.classifier.predict([user_input])[0]  # Wrap in list and get first prediction
        solution = self.knowledge_base.get_solution(user_input)
        if solution != "No solution found":
            return solution
        else:
            assigned_agent = self.route_ticket(user_input, category)
            return f"I understand you're having a {category} issue. I've created a ticket and assigned it to {assigned_agent}. They will contact you shortly."

    def create_ticket(self, name, email, title, description, priority):
        ticket_id = len(self.tickets) + 1
        category = self.classifier.predict([description])[0]
        assigned_agent = self.route_ticket(description, category)
        ticket = {
            "id": ticket_id,
            "title": title,
            'name': name,
            'email': email,
            "description": description,
            "priority": priority,
            "category": category,
            "assigned_agent": assigned_agent,
            "status": "Open"
        }
        self.tickets.append(ticket)
        self.save_ticket_to_csv(ticket)
        return ticket
    
    def save_ticket_to_csv(self, ticket):
        with open(self.csv_filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=ticket.keys())
            if file.tell() == 0:  # If file is empty, write header
                writer.writeheader()
            writer.writerow(ticket)

    def load_tickets_from_csv(self):
        try:
            with open(self.csv_filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.tickets = [dict(row) for row in reader]
                # Convert 'id' back to integer
                for ticket in self.tickets:
                    ticket['id'] = int(ticket['id'])
        except FileNotFoundError:
            self.tickets = []
    
    def route_ticket(self, description, category):
        matching_agents = [
            agent for agent, skills in self.agent_skills.items()
            if category in skills
        ]
        return random.choice(matching_agents) if matching_agents else "Unassigned"

    def get_recent_tickets(self, limit=5):
        return sorted(self.tickets, key=lambda x: x['id'], reverse=True)[:limit]

    def generate_insights(self):
        common_issues = predict_common_issues([t['description'] for t in self.tickets])
        performance_metrics = analyze_performance(self.tickets)
        return common_issues, performance_metrics