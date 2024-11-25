import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
# Initialize FastAPI app
app = FastAPI()

# Initialize Groq API client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Initialize SentenceTransformer for embeddings
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Dummy internal Wiki documents
wiki_docs = [
    {"id": 1, "title": "How to reset your password", 
     "content": "To reset your password, go to the settings page and click on 'Forgot Password'. Follow the instructions sent to your email."},
    {"id": 2, "title": "Setting up Two-Factor Authentication", 
     "content": "Two-factor authentication adds an extra layer of security. Go to your account settings and enable 2FA under the security section."},
    {"id": 3, "title": "API Rate Limiting", 
     "content": "API rate limits prevent abuse. Contact the admin team if you require higher limits for your application."},
    {"id": 4, "title": "Managing User Roles", 
     "content": "User roles determine access levels. Admins can assign or revoke roles under the 'User Management' section."},
    {"id": 5, "title": "Creating a New Project", 
     "content": "To create a new project, navigate to the 'Projects' page, click on 'Create New', and fill in the required details."},
    {"id": 6, "title": "Exporting Reports", 
     "content": "Reports can be exported as CSV or PDF. Go to the 'Reports' tab, select the desired report, and click on 'Export'."},
    {"id": 7, "title": "Configuring Webhooks", 
     "content": "Webhooks allow real-time communication with external services. Set up webhooks in the 'Integrations' section by providing the endpoint URL."},
    {"id": 8, "title": "Enabling Dark Mode", 
     "content": "To enable dark mode, go to the 'Settings' page, and toggle the 'Dark Mode' option under 'Preferences'."},
    {"id": 9, "title": "Understanding Data Backups", 
     "content": "Regular data backups ensure safety. Backups are created nightly and stored securely. Contact support for restoration requests."},
    {"id": 10, "title": "Troubleshooting Email Notifications", 
     "content": "If you're not receiving email notifications, check your spam folder or verify your email settings in the 'Notifications' tab."},
    {"id": 11, "title": "Setting Up a Custom Domain", 
     "content": "To set up a custom domain, navigate to the 'Domains' section, add your domain, and verify ownership via DNS."},
    {"id": 12, "title": "Managing API Keys", 
     "content": "API keys can be generated, revoked, or updated in the 'API Management' section under 'Developer Tools'."},
    {"id": 13, "title": "Monitoring System Logs", 
     "content": "System logs provide insights into application activities. Access logs from the 'System Logs' section in the admin panel."},
    {"id": 14, "title": "Customizing Notifications", 
     "content": "Notifications can be customized per user or globally. Configure settings in the 'Notifications' panel."},
    {"id": 15, "title": "Best Practices for Secure Passwords", 
     "content": "Use a mix of uppercase, lowercase, numbers, and special characters. Avoid using common words or patterns."},
    {"id": 16, "title": "Integrating with Slack", 
     "content": "To integrate with Slack, go to 'Integrations', select Slack, and follow the OAuth setup process."},
    {"id": 17, "title": "Managing Billing Information", 
     "content": "Update billing information under 'Account Settings'. Ensure valid payment methods to avoid service interruptions."},
    {"id": 18, "title": "Data Privacy Guidelines", 
     "content": "Our platform complies with GDPR and CCPA. Review the 'Privacy Policy' for details on data handling."},
    {"id": 19, "title": "Accessing Archived Data", 
     "content": "Archived data can be retrieved by navigating to the 'Archives' section. Use filters to find specific data."},
    {"id": 20, "title": "Understanding User Analytics", 
     "content": "Analytics provide insights into user activity. Access detailed reports from the 'Analytics' dashboard."},
    {"id": 21, "title": "Enabling Beta Features", 
     "content": "Beta features can be enabled in 'Settings' under the 'Advanced' tab. Note that beta features are experimental."},
    {"id": 22, "title": "Setting Up Single Sign-On (SSO)", 
     "content": "SSO can be configured via 'Authentication Settings'. Follow the provided instructions to integrate your SSO provider."},
    {"id": 23, "title": "Customizing User Profiles", 
     "content": "Users can personalize their profiles with avatars and bios. Changes can be made in 'Profile Settings'."},
    {"id": 24, "title": "Understanding Account Deactivation", 
     "content": "Deactivating an account disables all access. Admins can reactivate accounts under 'User Management'."},
    {"id": 25, "title": "Adding Multi-Language Support", 
     "content": "Enable multi-language support in 'Settings'. Select supported languages for the user interface."},
    {"id": 26, "title": "Integrating Payment Gateways", 
     "content": "Payment gateways like Stripe and PayPal can be configured in the 'Payments' section."},
    {"id": 27, "title": "Optimizing Performance", 
     "content": "Performance optimization tips include caching frequently accessed data and reducing API call frequency."},
    {"id": 28, "title": "Resolving 404 Errors", 
     "content": "404 errors occur when a resource is not found. Ensure the correct URL is used or contact support."},
    {"id": 29, "title": "Understanding Version Control", 
     "content": "Version control tracks changes to documents. View version history under 'Document Settings'."},
    {"id": 30, "title": "Migrating Data to the Platform", 
     "content": "Data migration can be performed using our import tools. Refer to the 'Data Migration Guide' for details."}
]


# Precompute document embeddings
doc_texts = [f"{doc['title']}: {doc['content']}" for doc in wiki_docs]
doc_embeddings = embedder.encode(doc_texts, convert_to_tensor=False)
doc_embeddings = np.array(doc_embeddings, dtype='float32')

# Initialize FAISS index
dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(doc_embeddings)

# Request model payload
class QueryRequest(BaseModel):
    query: str

@app.post("/qna")
async def qna_endpoint(request: QueryRequest):
    try:
        # Embed the query and search for the most relevant context
        query_embedding = embedder.encode(request.query, convert_to_tensor=False).astype('float32')
        k = 3  # Number of top results to retrieve
        distances, indices = index.search(query_embedding.reshape(1, -1), k)

        # Retrieve relevant contexts
        contexts = [doc_texts[idx] for idx in indices[0]]

        # Combine context with the query
        context_text = "\n".join(contexts)
        prompt = f"Answer should contain important data from the context. Context: {context_text}\n\nQuestion: {request.query}\n\nAnswer:"

        # Make a call to the Groq AI model
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192"
        )

        # Extract the AI's response
        result = chat_completion.choices[0].message.content

        return {"query": request.query, "context": contexts, "response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/autocomplete")
async def autocomplete_endpoint(request: QueryRequest):
    try:
        # Embed the query and search for the most relevant contexts
        query_embedding = embedder.encode(request.query, convert_to_tensor=False).astype('float32')
        k = 3  # Number of top suggestions to retrieve
        distances, indices = index.search(query_embedding.reshape(1, -1), k)

        # Retrieve relevant contexts
        suggestions = [wiki_docs[idx]['title'] for idx in indices[0]]

        return {"query": request.query, "suggestions": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app with `uvicorn` (e.g., `uvicorn main:app --reload`)
