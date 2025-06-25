# Marketing KPI Definitions and SQL Queries

## Core Marketing Performance KPIs

### 1. ROAS (Return on Ad Spend)
**Definition**: Revenue generated per dollar spent on advertising
**Calculation**: purchase_revenue / spend_amount
**Good Benchmark**: >3.0 for e-commerce, >4.0 for mature campaigns
**Business Impact**: Direct measure of advertising profitability




### 2. CAC (Customer Acquisition Cost)
**Definition**: Cost to acquire one new customer (signup)
**Calculation**: spend_amount / signups
**Good Benchmark**: <20% of Customer LTV, typically $10-50 for e-commerce
**Business Impact**: Critical for understanding customer acquisition efficiency



### 3. CTR (Click-Through Rate)
**Definition**: Percentage of impressions that result in clicks
**Calculation**: (clicks / impressions) * 100
**Good Benchmark**: >2% for search, >0.5% for display, >1% for social
**Business Impact**: Measures ad relevance and creative effectiveness



## Conversion Funnel KPIs

### 4. Purchase Conversion Rate
**Definition**: Percentage of clicks that result in purchases
**Calculation**: (purchase_count / clicks) * 100
**Good Benchmark**: >2-5% for e-commerce
**Business Impact**: Measures bottom-funnel effectiveness



### 5. Signup Conversion Rate
**Definition**: Percentage of clicks that result in account creation
**Calculation**: (signups / clicks) * 100
**Good Benchmark**: >5-15% for e-commerce
**Business Impact**: Measures top-funnel lead generation effectiveness



## Advanced Marketing KPIs

### 6. Session-to-Purchase Rate
**Definition**: Percentage of sessions that result in purchases
**Calculation**: (sessions_purchase / total_sessions) * 100
**Good Benchmark**: >1-3% for e-commerce
**Business Impact**: Measures website conversion effectiveness


### 7. Cost Per Acquisition (CPA) by Conversion Type
**Definition**: Cost to achieve specific conversion actions
**Calculation**: spend_amount / conversions
**Good Benchmark**: Varies by conversion type and industry
**Business Impact**: Optimizes budget allocation across conversion goals



### 8. Revenue Per Click (RPC)
**Definition**: Average revenue generated per click
**Calculation**: purchase_revenue / clicks
**Good Benchmark**: Should exceed CPC for profitability
**Business Impact**: Measures click quality and revenue efficiency



### 9. Customer Lifetime Value to CAC Ratio (LTV:CAC)
**Definition**: Ratio of customer lifetime value to acquisition cost
**Calculation**: Estimated LTV / CAC
**Good Benchmark**: >3:1, ideally >5:1
**Business Impact**: Determines sustainable growth potential



### 10. Marketing Efficiency Score
**Definition**: Composite score measuring overall marketing effectiveness
**Calculation**: Weighted average of key performance metrics
**Good Benchmark**: >70 for efficient campaigns
**Business Impact**: Holistic view of marketing performance



## Performance Monitoring Queries

### 11. Weekly Performance Trends


### 12. Campaign Performance Alert System


## Query Performance Optimization Notes

1. **Use Date Filters**: Always include date ranges to limit scan scope
2. **Index Recommendations**: Ensure indexes on (date, campaign_id, channel)
3. **Aggregation First**: Use CTEs to pre-aggregate before complex calculations
4. **NULLIF Usage**: Prevent division by zero errors
5. **HAVING Clauses**: Filter aggregated results to focus on significant data
6. **Partitioned Analysis**: Use window functions for trend analysis

## KPI Refresh Schedule Recommendations

- **Real-time**: CTR, Impressions, Clicks (for active campaign monitoring)
- **Daily**: ROAS, CAC, Conversion Rates (for daily optimization)
- **Weekly**: LTV:CAC, Marketing Efficiency Score (for strategic decisions)
- **Monthly**: Cohort analysis, Long-term trend analysis