# Database Schema Overview

## Schema Architecture
- **public**: Raw, unprocessed data (NEVER use for business reporting)
- **public_staging**: Cleaned and standardized data (intermediate processing)
- **public_marts**: Business-ready, aggregated data (PRIMARY source for analytics)

## Data Flow
Raw Data (public) → Staging (public_staging) → Marts (public_marts) → Reports

## Key Principles
1. Always use public_marts for business KPIs
2. Only reference staging for debugging/validation
3. Never use raw tables for business insights
