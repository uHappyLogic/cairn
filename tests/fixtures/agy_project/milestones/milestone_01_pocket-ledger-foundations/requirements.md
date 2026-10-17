# Milestone 1: Pocket Ledger Foundations

## Goal

Build Pocket Ledger, a command-line tool that records personal expenses and prints a summary of them. A user adds one expense at a time with an amount, a category, and a date, and asks for the total per category over a period. This milestone delivers the first working version: recording and summarizing, nothing more.

## Relevant starting state

The repository holds only the milestone files under `milestones/`; no source code, configuration, or documentation exists yet. The ledger will be one Python 3.9+ script using the standard library alone, run from a terminal, keeping its data in a single file inside the user's home directory. The person using it tracks a few dozen expenses a month in one currency and reads the summary at month end.

## Decisions

- **One stdlib-only Python script.** The ledger is a single Python 3.9+ file with no third-party dependency, so it runs wherever a Python interpreter does.
- **One data file per user.** Every entry lives in one file under the user's home directory; the ledger never spreads its data over several files.

## Out of Scope

- A graphical or web interface.
- Multi-currency entries and exchange rates.
- Synchronizing the data file between machines.
