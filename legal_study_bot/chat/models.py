from django.db import models


class ConversationSummary(models.Model):
    """
    Stores summarized conversation context per case
    """

    session_id = models.CharField(max_length=100)
    case_id = models.CharField(max_length=500)

    summary = models.TextField()

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("session_id", "case_id")

    def __str__(self):
        return f"{self.session_id} | {self.case_id}"
