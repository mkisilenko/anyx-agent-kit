# Anyx workflow prompts

**TLDR:** Set the group and time once. Run the selected workflow through the connected Anyx MCP client. These are prompt templates, not live results.

## Team catch-up

```text
Use anyx-team-catchup for my selected project group over the last 24 hours.
Return decisions, accepted commitments and open questions with sources.
Keep the result in this conversation.
```

```text
הפעל anyx-team-catchup על הקבוצה שבחרתי ב-24 השעות האחרונות.
הצג החלטות, התחייבויות ושאלות פתוחות עם מקורות. השאר כאן.
```

## Materials review

```text
Use anyx-materials-review for the selected maintenance group today.
Keep quantities by exact item, unit and job. Preserve corrections and gaps.
Prepare a supplier inquiry draft here for my review. Do not send it.
```

```text
הפעל anyx-materials-review על הקבוצה שבחרתי להיום.
שמור כמויות לפי דגם, יחידה ועבודה, כולל תיקונים ופרטים חסרים.
הכן כאן טיוטת בירור לספק לבדיקה שלי.
```

## Decision log

```text
Use anyx-decision-log for project J42 in the selected group this week.
Show approvals, conditions, withdrawals and unresolved authority questions.
Retain the earlier entry when a later authorized decision replaces it.
```

```text
הפעל anyx-decision-log לפרויקט J42 בקבוצה שבחרתי השבוע.
הצג אישורים, תנאים, ביטולים ומחלוקות פתוחות, עם מקורות.
```

Connect through the [Anyx MCP quickstart](https://docs.anyx.app/developers/mcp-quickstart). Group selection is a usage filter; the credential can cover all eligible active groups owned by the account. No personal key belongs in a prompt.

