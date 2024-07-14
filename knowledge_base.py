class KnowledgeBase:
    def __init__(self):
        self.articles = {
            "network issue": "Please try resetting your router and reconnecting to the network.",
            "password reset": "You can reset your password by visiting our self-service portal at example.com/reset.",
            "software bug": "Please try updating the software to the latest version and restart your computer.",
        }
        
    def add_article(self, issue, solution):
        self.articles[issue] = solution
        
    def get_solution(self, issue):
        # Simple keyword matching for demonstration
        for key, value in self.articles.items():
            if key in issue.lower():
                return value
        return "No solution found"
    
    def update_from_resolved_ticket(self, ticket, solution):
        self.add_article(ticket, solution)