"""Parser for Jira ticket XML files."""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any
from ..models.jira_models import (
    JiraTicket,
    JiraUser,
    JiraStatus,
    JiraPriority,
    JiraTicketType,
    JiraComponent,
    JiraLabel,
    JiraHistoryChange,
)


def parse_jira_xml(xml_path: str | Path) -> List[JiraTicket]:
    """
    Parse Jira tickets from XML file.
    
    Args:
        xml_path: Path to the XML file containing Jira tickets
        
    Returns:
        List of JiraTicket objects with full temporal information
    """
    xml_path = Path(xml_path)
    if not xml_path.exists():
        raise FileNotFoundError(f"XML file not found: {xml_path}")
    
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    tickets = []
    # Cache for reusing user, status, priority, type objects
    users_cache: Dict[str, JiraUser] = {}
    status_cache: Dict[str, JiraStatus] = {}
    priority_cache: Dict[str, JiraPriority] = {}
    type_cache: Dict[str, JiraTicketType] = {}
    component_cache: Dict[str, JiraComponent] = {}
    label_cache: Dict[str, JiraLabel] = {}
    
    for ticket_elem in root.findall('ticket'):
        # Parse basic fields
        ticket_id = _get_text(ticket_elem, 'id')
        key = _get_text(ticket_elem, 'key')
        summary = _get_text(ticket_elem, 'summary')
        description = _get_text(ticket_elem, 'description')
        
        # Parse status
        status_name = _get_text(ticket_elem, 'status')
        if status_name not in status_cache:
            status_cache[status_name] = JiraStatus(name=status_name)
        status = status_cache[status_name]
        
        # Parse priority
        priority_name = _get_text(ticket_elem, 'priority')
        if priority_name not in priority_cache:
            priority_cache[priority_name] = JiraPriority(name=priority_name)
        priority = priority_cache[priority_name]
        
        # Parse type
        type_name = _get_text(ticket_elem, 'type')
        if type_name not in type_cache:
            type_cache[type_name] = JiraTicketType(name=type_name)
        ticket_type = type_cache[type_name]
        
        # Parse users
        reporter_email = _get_text(ticket_elem, 'reporter')
        if reporter_email not in users_cache:
            users_cache[reporter_email] = JiraUser(email=reporter_email)
        reporter = users_cache[reporter_email]
        
        assignee_email = _get_text(ticket_elem, 'assignee')
        assignee = None
        if assignee_email:
            if assignee_email not in users_cache:
                users_cache[assignee_email] = JiraUser(email=assignee_email)
            assignee = users_cache[assignee_email]
        
        # Parse timestamps
        created_date = _get_text(ticket_elem, 'created')
        updated_date = _get_text(ticket_elem, 'updated')
        resolved_date = _get_text(ticket_elem, 'resolved') or None
        
        # Parse components
        components = []
        components_elem = ticket_elem.find('components')
        if components_elem is not None:
            for comp_elem in components_elem.findall('component'):
                comp_name = comp_elem.text
                if comp_name:
                    if comp_name not in component_cache:
                        component_cache[comp_name] = JiraComponent(name=comp_name)
                    components.append(component_cache[comp_name])
        
        # Parse labels
        labels = []
        labels_elem = ticket_elem.find('labels')
        if labels_elem is not None:
            for label_elem in labels_elem.findall('label'):
                label_name = label_elem.text
                if label_name:
                    if label_name not in label_cache:
                        label_cache[label_name] = JiraLabel(name=label_name)
                    labels.append(label_cache[label_name])
        
        # Parse history
        history = []
        history_elem = ticket_elem.find('history')
        if history_elem is not None:
            for change_elem in history_elem.findall('change'):
                timestamp = _get_text(change_elem, 'timestamp')
                field = _get_text(change_elem, 'field')
                from_value = _get_text(change_elem, 'from')
                to_value = _get_text(change_elem, 'to')
                author_email = _get_text(change_elem, 'author')
                
                if author_email not in users_cache:
                    users_cache[author_email] = JiraUser(email=author_email)
                author = users_cache[author_email]
                
                change = JiraHistoryChange(
                    timestamp=timestamp,
                    field=field,
                    from_value=from_value,
                    to_value=to_value,
                    author=author
                )
                history.append(change)
        
        # Create ticket
        ticket = JiraTicket(
            ticket_id=ticket_id,
            key=key,
            summary=summary,
            description=description,
            status=status,
            priority=priority,
            ticket_type=ticket_type,
            reporter=reporter,
            assignee=assignee,
            created_date=created_date,
            updated_date=updated_date,
            resolved_date=resolved_date,
            components=components,
            labels=labels,
            history=history
        )
        tickets.append(ticket)
    
    return tickets


def _get_text(element: ET.Element, tag: str) -> str:
    """Helper to safely extract text from XML element."""
    child = element.find(tag)
    return child.text if child is not None and child.text else ""
