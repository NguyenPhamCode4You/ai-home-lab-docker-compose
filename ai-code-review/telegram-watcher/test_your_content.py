#!/usr/bin/env python3
"""
Test script specifically for your checklist content to show the exact formatting.
"""

import sys
import os

# Add the directory containing run.py to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from run import format_markdown_for_telegram

def test_your_exact_content():
    """Test with your exact checklist content"""
    
    your_content = """## 📋 Checklist by C4Y-AI

*Performed by:* C4Y-AI (ai@c4y.com)
*Date:* 2025-07-07 23:17:00 UTC
*Type:* Checklist Review

### Summary
Fixes for laytime calculation logic and updates to data transfer objects.

### Checklist Overview (Mark the applicable categories with checkboxes)
- [ ] 1. Project Structure Changes
- [ ] 2. Dependencies & Libraries
- [x] 3. APIs & Controllers
- [x] 4. Business Logics
- [ ] 5. Infrastructure & Configuration
- [x] 6. Data Entities & DTOs
- [x] 7. Security & Concerns
- [ ] 8. Database Migration & Query Performance
- [ ] 9. Unit & Integration Tests
- [ ] 10. Code Quality

### Detailed Review

*APIs & Controllers*
- *LaytimeCalculationsController.cs*: ✅ New using directive for `Core.Infrastructure.Security` -
necessary for security features.

*Business Logics*
- *CreateLaytimeGroup.cs*: ⚠️ Removed unused `using Core.Domain.MasterData.Entities;`.
- *GetAllClaimInfoItemsByVoyageId.cs*: ✅ Added `using Microsoft.IdentityModel.Tokens;` - necessary
for token handling.
- *GetAllItineraryItemsByVoyageId.cs*: ✅ Improved method to handle voyage retrieval with additional
fields included."""

    print("🔄 BEFORE FORMATTING (Raw markdown):")
    print("-" * 60)
    print(your_content)
    print("\n" + "="*80 + "\n")
    
    print("✨ AFTER FORMATTING (Telegram-ready):")
    print("-" * 60)
    formatted = format_markdown_for_telegram(your_content)
    print(formatted)
    print("\n" + "="*80 + "\n")
    
    print("📱 COMPLETE TELEGRAM MESSAGE (as it will appear):")
    print("-" * 60)
    
    complete_message = f"""✅ *Checklist Completed*
📁 Project: `my-project`
🔀 MR: `123`

📝 *Checklist Content:*
{formatted}

🔗 [View on GitLab](https://gitlab.example.com/project/merge_requests/123)"""
    
    print(complete_message)
    print(f"\nTotal message length: {len(complete_message)} characters")
    print("(Telegram limit: 4096 characters)")

if __name__ == "__main__":
    test_your_exact_content()
