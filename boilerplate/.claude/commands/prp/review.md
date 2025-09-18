# PRP Review & Completion

## PRP File: $ARGUMENTS

## MAIN MISSION

Verify and review harshly if we successfully implemented the PRP specified in $ARGUMENTS. Use all agents, MCPs and commands at your disposal. This is the final check before marking the PRP as COMPLETED! This will define our brand and will be the cornerstone of customer perception in terms of style, character, grit and quality.

## Review Process

1. **Load PRP & Check Current Status**
   - Read the specified PRP file
   - Verify current status is `IN_PROGRESS`
   - If not, warn that review is typically for IN_PROGRESS PRPs

2. **Comprehensive Review**
   - Verify all Success Criteria from the PRP are met
   - Check all Implementation Tasks were completed
   - Run all validation levels from the PRP
   - Ensure all Architecture Decision Records (ADR) in docs/adr/ have been followed
   - If diverging from ADRs, ensure it's reasoned and documented

3. **Update Status on Success**
   - If review passes: Update `Status: IN_PROGRESS` to `Status: COMPLETED`
   - Update `Status_Date:` to today's date
   - Add `Status_Note: Review passed - all criteria met`
   - If review fails: Leave as IN_PROGRESS and provide detailed feedback

## NOTEs

- $ARGUMENTS should be a reference to a PRP file. If none provided, ask the user to provide one.
- Only mark as COMPLETED if all criteria genuinely pass the harsh review