from django.db import models
import sqlite3

# class ConversationSummary(models.Model):
#     """
#     Stores summarized conversation context per case
#     """

#     session_id = models.CharField(max_length=100)
#     case_id = models.CharField(max_length=500)

#     summary = models.TextField()

#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         unique_together = ("session_id", "case_id")

class CachedResponse(models.Model):
    """
    Stores cached responses for case queries
    """
    case_name = models.CharField(max_length=500)
    query = models.TextField()
    response = models.TextField()

    class Meta:
        unique_together = ("case_name", "query")

    def __str__(self):
        return f"{self.case_name} | {self.query[:50]}"
    


# class CachedResponse(models.Model):    

#     case_name = models.CharField(max_length=100)
#     query = models.TextField()  
#     response = models.TextField()       
    
#     class Meta:
#         unique_together = ("case_name", "query")

#     def __str__(self):
#         return f"Cache for {self.case_name} | Query: {self.query[:30]}..."