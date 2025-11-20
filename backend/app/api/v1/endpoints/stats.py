"""Statistics and dashboard endpoints."""
from datetime import datetime, timedelta
from typing import Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.entry import Entry, EntryStatus, SeverityLevel, WorkflowState
from app.models.tag import EntryTag, Tag
from app.models.user import User

router = APIRouter()


@router.get("/")
async def get_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict:
    """Get dashboard statistics."""
    
    # Total entries count
    total_result = await db.execute(select(func.count(Entry.id)))
    total_entries = total_result.scalar() or 0
    
    # Active entries count
    active_result = await db.execute(
        select(func.count(Entry.id)).where(Entry.status == EntryStatus.ACTIVE)
    )
    active_entries = active_result.scalar() or 0
    
    # Archived entries count
    archived_result = await db.execute(
        select(func.count(Entry.id)).where(Entry.status == EntryStatus.ARCHIVED)
    )
    archived_entries = archived_result.scalar() or 0
    
    # Critical entries count
    critical_result = await db.execute(
        select(func.count(Entry.id)).where(Entry.severity == SeverityLevel.CRITICAL)
    )
    critical_entries = critical_result.scalar() or 0
    
    # Severity distribution
    severity_distribution = {}
    for severity in SeverityLevel:
        result = await db.execute(
            select(func.count(Entry.id)).where(Entry.severity == severity)
        )
        count = result.scalar() or 0
        severity_distribution[severity.value] = count
    
    # Workflow state distribution
    workflow_distribution = {}
    for state in WorkflowState:
        result = await db.execute(
            select(func.count(Entry.id)).where(Entry.workflow_state == state)
        )
        count = result.scalar() or 0
        workflow_distribution[state.value] = count
    
    # Status distribution
    status_distribution = {}
    for status in EntryStatus:
        result = await db.execute(
            select(func.count(Entry.id)).where(Entry.status == status)
        )
        count = result.scalar() or 0
        status_distribution[status.value] = count
    
    # Top tags by usage
    tag_usage_result = await db.execute(
        select(Tag.id, Tag.name, Tag.color, func.count(EntryTag.id).label('count'))
        .join(EntryTag, Tag.id == EntryTag.tag_id)
        .group_by(Tag.id, Tag.name, Tag.color)
        .order_by(func.count(EntryTag.id).desc())
        .limit(10)
    )
    top_tags = [
        {
            "id": str(row[0]),
            "name": row[1],
            "color": row[2],
            "count": row[3]
        }
        for row in tag_usage_result.all()
    ]
    
    # Recent entries count (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_result = await db.execute(
        select(func.count(Entry.id))
        .where(Entry.created_at >= thirty_days_ago)
    )
    recent_entries = recent_result.scalar() or 0
    
    return {
        "total_entries": total_entries,
        "active_entries": active_entries,
        "archived_entries": archived_entries,
        "critical_entries": critical_entries,
        "recent_entries": recent_entries,
        "severity_distribution": severity_distribution,
        "workflow_distribution": workflow_distribution,
        "status_distribution": status_distribution,
        "top_tags": top_tags
    }

