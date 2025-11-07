# Personal Assistant Capabilities Reference

## Core Capabilities

This document provides detailed information about the personal assistant's capabilities and how to leverage them effectively.

## 1. Profile Management

### Profile Components

**Personal Information:**
- Name and preferred form of address
- Timezone and location
- Contact preferences

**Work & Schedule:**
- Working hours (start, end, flexibility)
- Work environment (office, remote, hybrid)
- Break preferences
- Meeting preferences
- Preferred working times

**Goals & Priorities:**
- Short-term goals (1-3 months)
- Long-term goals (6+ months)
- Priority areas
- Success metrics and KPIs

**Habits & Routines:**
- Morning routine
- Evening routine
- Exercise habits
- Sleep schedule
- Meal patterns
- Self-care practices

**Communication Preferences:**
- Communication style (concise, detailed, balanced)
- Reminder style (gentle, firm, assertive)
- Notification preferences
- Preferred communication channels

**Tools & Systems:**
- Calendar system
- Task management tools
- Note-taking apps
- Email client
- Other productivity tools

## 2. Task Management

### Task Properties

Every task can include:
- **Title** (required): Brief description
- **Description** (optional): Detailed information
- **Priority**: high, medium, low
- **Category**: work, personal, health, learning, etc.
- **Due Date**: ISO format (YYYY-MM-DD)
- **Estimated Time**: Duration to complete
- **Status**: pending, in_progress, completed
- **Dependencies**: Related tasks or prerequisites
- **Tags**: Custom labels for organization

### Task Organization Strategies

**By Priority:**
- High priority tasks first
- Consider urgency vs importance
- Eisenhower Matrix approach

**By Category:**
- Group similar tasks together
- Context-switching optimization
- Focus on one area at a time

**By Time:**
- Chronological ordering
- Deadline-driven
- Time-blocking compatible

**By Energy:**
- High-energy tasks during peak hours
- Low-energy tasks during slow periods
- Match task difficulty to energy levels

### Task Lifecycle

1. **Creation**: Task is added with initial details
2. **Planning**: Due date, priority, and category assigned
3. **Scheduling**: Task placed in calendar/schedule
4. **Execution**: Task marked in progress
5. **Completion**: Task marked complete and archived
6. **Review**: Periodic review of completed tasks

## 3. Schedule Management

### Event Types

**One-Time Events:**
- Appointments
- Deadlines
- Special occasions
- Travel
- Social events

**Recurring Events:**
- Daily standups
- Weekly meetings
- Regular exercise
- Classes or courses
- Maintenance tasks

### Schedule Optimization

**Time Blocking:**
- Dedicated blocks for focused work
- Buffer time between meetings
- Break blocks for rest
- Flexible blocks for unexpected tasks

**Energy Management:**
- Schedule important tasks during peak energy times
- Lighter tasks during low-energy periods
- Regular breaks to maintain energy
- Align task type with energy level

**Conflict Resolution:**
- Identify scheduling conflicts proactively
- Suggest alternative times
- Consider priority when resolving
- Maintain work-life balance

## 4. Context and Memory Management

### Context Types

**Recent Interactions:**
- Recent conversations
- Decisions made
- Information shared
- Standard retention: 30 days
- High importance: Kept longer

**Important Notes:**
- Key preferences
- Critical information
- Long-term references
- Never auto-deleted
- Always available

**Temporary Context:**
- Short-term projects
- Current focus areas
- Transient information
- Auto-cleaned after 7 days
- For immediate continuity

### Context Importance Levels

**Low Importance:**
- Routine interactions
- Minor details
- Quick cleanup (7-14 days)

**Normal Importance:**
- Standard interactions
- Regular updates
- Medium retention (30 days)

**High Importance:**
- Critical information
- Key preferences
- Long-term or indefinite retention

### Intelligent Data Retention

The system automatically:
- Removes outdated completed tasks
- Cleans up old temporary context
- Archives past events
- Retains important notes indefinitely
- Keeps high-importance items longer

Manual cleanup can be triggered:
- Monthly recommended
- Custom retention periods
- Selective cleanup options

## 5. Personalization Strategies

### Communication Adaptation

**Concise Style:**
- Brief, to-the-point responses
- Bullet points and lists
- Action-oriented
- Minimal elaboration

**Detailed Style:**
- Comprehensive explanations
- Context and reasoning
- Multiple options explained
- Thorough background

**Balanced Style:**
- Mix of brief and detailed
- Context when needed
- Summary + details available
- Flexible approach

### Recommendation Personalization

**Based on Goals:**
- Connect tasks to objectives
- Prioritize goal-aligned activities
- Track progress toward goals
- Celebrate milestones

**Based on Schedule:**
- Respect working hours
- Consider availability
- Account for energy patterns
- Avoid conflicts

**Based on Preferences:**
- Honor communication style
- Follow organization preferences
- Respect boundaries
- Adapt to feedback

### Proactive Assistance

**Anticipate Needs:**
- Remind about upcoming deadlines
- Suggest task prioritization
- Flag potential conflicts
- Propose optimizations

**Provide Context:**
- Reference previous interactions
- Connect to goals
- Explain reasoning
- Offer alternatives

**Learn and Adapt:**
- Track what works
- Adjust recommendations
- Refine approach
- Improve over time

## 6. Productivity Insights

### Time Management

**Focus Time:**
- Identify peak productivity hours
- Schedule important work accordingly
- Minimize interruptions during focus time
- Protect deep work blocks

**Meeting Management:**
- Batch meetings when possible
- Maintain meeting-free days
- Limit meeting duration
- Ensure meeting necessity

**Break Optimization:**
- Regular breaks prevent burnout
- Pomodoro technique support
- Active vs passive breaks
- Movement and rest balance

### Goal Tracking

**Progress Monitoring:**
- Regular check-ins on goals
- Milestone celebrations
- Adjustment when needed
- Obstacle identification

**Habit Formation:**
- Consistency over intensity
- Small wins compound
- Track streaks
- Build on success

**Accountability:**
- Regular progress reports
- Gentle reminders
- Success reinforcement
- Course correction support

## 7. Best Use Cases

### Daily Planning

"What should I focus on today?"
- Reviews pending tasks
- Checks schedule
- Considers goals
- Suggests priorities

### Weekly Review

"Help me plan my week"
- Overview of commitments
- Task distribution
- Goal alignment
- Balance check

### Task Overwhelm

"I have too much to do"
- Prioritization assistance
- Breaking down large tasks
- Delegation suggestions
- Realistic scheduling

### Goal Setting

"Help me achieve X"
- Break down goal
- Create action plan
- Schedule activities
- Track progress

### Schedule Conflicts

"I need to reschedule X"
- Find alternatives
- Consider priorities
- Minimize disruption
- Propose solutions

### Productivity Coaching

"I'm not being productive"
- Analyze patterns
- Identify blockers
- Suggest strategies
- Provide support

## 8. Integration Tips

### Calendar Sync

While the assistant maintains its own schedule, it works best when:
- You mention calendar updates
- You reference external calendars
- You sync important events manually
- You keep the assistant informed

### Task System Sync

For best results:
- Add tasks as they arise
- Update status regularly
- Review completed tasks
- Archive when appropriate

### Note-Taking Integration

Complement existing systems:
- Important notes → assistant context
- Project notes → task descriptions
- Meeting notes → event details
- Reference notes → profile updates

## 9. Privacy and Data Management

### Data Location

All data stored locally:
- `~/.claude/personal_assistant/`
- User-owned and controlled
- No external syncing
- Easily exportable

### Data Export

Export all data anytime:
```bash
python3 scripts/assistant_db.py export > backup.json
```

### Data Reset

Complete reset if needed:
```bash
python3 scripts/assistant_db.py reset
```

### Selective Cleanup

Remove old data while keeping important items:
```bash
python3 scripts/assistant_db.py cleanup 30
```

## 10. Advanced Features

### Batch Operations

Perform multiple actions:
- Add multiple tasks at once
- Schedule multiple events
- Update multiple preferences
- Bulk task completion

### Smart Reminders

Context-aware reminders:
- Consider location
- Check schedule
- Account for dependencies
- Respect preferences

### Habit Tracking

Build and maintain habits:
- Daily habit check-ins
- Streak tracking
- Completion patterns
- Obstacle identification

### Energy Mapping

Optimize based on energy:
- Track energy patterns
- Schedule accordingly
- Identify energy drains
- Maximize peak times

### Goal Cascading

Break down large goals:
- Major goal → sub-goals
- Sub-goals → action items
- Action items → scheduled tasks
- Scheduled tasks → completed actions
