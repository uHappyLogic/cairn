# Karpathy wrapped Cairn multisprint orchestration

## Flow

```mermaid
sequenceDiagram
autonumber

actor Stakeholder
participant IdeaDocument
actor DeliverableTeam
participant Karpathy
participant Cairn
participant Deliverable

Stakeholder->>IdeaDocument: Define idea
DeliverableTeam->>IdeaDocument: Reads document 
DeliverableTeam->>Karpathy: Feed the idea document
DeliverableTeam->>Karpathy: Define<br/>Definition Of Done<br/>for given idea
DeliverableTeam->>Karpathy: Start execution loop

loop Until DoD not done
    Karpathy->>Karpathy: Evaluate DoD result
    Karpathy->>Cairn: Create milestones for work delta
    Karpathy->>Cairn: Execute milestones
    Cairn->>DeliverableTeam: Ask questions on<br/>implementation level design gaps
    DeliverableTeam->>Cairn: Provides answers
    Cairn->>Deliverable: Carry out work
end

DeliverableTeam->>Stakeholder: Present deliverable
```

## Handling transitions

It seems to me that the "Karpathy" should be an orchestrator that runs Cairn through CLI commands (as per ways-of-using-cairn). Specifically it shouldn't drive them in his own context.