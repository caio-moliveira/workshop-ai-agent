# Table Definitions and Business Context

## Marts Tables (public_marts)

### fct_campaign_daily_performance
**Description**: Daily campaign performance metrics combining marketing spend and website session engagement.
      Includes top-of-funnel metrics (page views, product views, cart, checkout, etc.) and marketing KPIs (CTR, CPC, CPS).
**Purpose**: Daily aggregated marketing campaign performance metrics
**Grain**: One row per campaign per day
**Key Columns**:
  - name: date
    description: Date of the campaign activity.
  - name: campaign_id
    description: Unique identifier of the marketing campaign.
  - name: channel
    description: Marketing channel used in the campaign.
  - name: ad_group
    description: Specific ad group within the campaign.
  - name: creative_type
    description: Type of creative used in the campaign (e.g., banner, video).
  - name: spend_amount
    description: Total spend in dollars for the campaign on that date.
  - name: impressions
    description: Number of ad impressions served.
  - name: clicks
    description: Number of ad clicks received.
  - name: total_sessions
    description: Total number of unique website sessions attributed to the campaign.
  - name: sessions_page_view
    description: Sessions where a page view occurred.
  - name: sessions_product_view
    description: Sessions where a product view occurred.
  - name: sessions_account_page
    description: Sessions where the account page was viewed.
  - name: sessions_checkout_start
    description: Sessions where checkout was initiated.
  - name: sessions_cart_view
    description: Sessions where the cart was viewed.
  - name: sessions_purchase
    description: Sessions that completed a purchase.
  - name: sessions_account_view
    description: Sessions that visited the account overview.
  - name: ctr
    description: Click-through rate (clicks divided by impressions).
  - name: cpc
    description: Cost per click.
  - name: cps
    description: Cost per session (spend divided by total sessions).

### fct_campaign_conversion_rates
**Description**: Campaign conversion performance metrics combining marketing spend, signups, and purchases.
      Helps evaluate conversion efficiency and campaign ROI.
**Purpose**: Campaign conversion funnel analysis
**Grain**: One row per campaign per conversion type
**Key Columns**:
  - name: date
    description: Date of the campaign activity.
  - name: campaign_id
    description: Unique identifier of the marketing campaign.
  - name: clicks
    description: Number of ad clicks received.
  - name: spend_amount
    description: Total spend in dollars for the campaign on that date.
  - name: signups
    description: Number of customer accounts created.
  - name: purchase_count
    description: Number of purchases made.
  - name: purchase_revenue
    description: Revenue generated from purchases.
  - name: total_conversions
    description: Combined total of signups and purchases.
  - name: signup_per_click
    description: Signup conversion rate (signups divided by clicks).
  - name: purchase_per_click
    description: Purchase conversion rate (purchases divided by clicks).
  - name: blended_conversion_rate
    description: Total conversion rate (signups + purchases) divided by clicks.
  - name: cpc
    description: Cost per click.
  - name: cost_per_signup
    description: Cost per account creation.
  - name: cost_per_purchase
    description: Cost per purchase.
  - name: cost_per_conversion
    description: Cost per blended conversion (signups + purchases).
  - name: roas
    description: Return on ad spend (purchase revenue divided by spend).
  - name: daily_margin
    description: Net daily revenue after subtracting ad spend.

## Staging Tables (public_staging)

### stg_customer_accounts
**Description**: Standardized and cleaned version of customer account data, derived from the seed CSV.
**Purpose**: Cleaned customer account data
**Key Columns**:
  - name: customer_id
    description: Unique identifier for the customer (renamed from account_id).
  - name: email
    description: Normalized email address of the user.
  - name: registered_at
    description: Timestamp when the customer registered (converted from string).
  - name: registration_source
    description: Origin platform of the registration (e.g., website, app).
  - name: utm_source
     description: UTM source from the customer's registration session.
  - name: utm_medium
     description: UTM medium used in the campaign that led to registration.
  - name: utm_campaign
    description: UTM campaign name for tracking.
  - name: utm_content
    description: UTM content used to differentiate creatives.
  - name: first_name
    description: Capitalized first name of the user.
  - name: last_name
    description: Capitalized last name of the user.
  - name: birth_year
    description: Year the customer was born.
  - name: country
    description: Country of the customer, formatted in upper case.
  - name: referral_code
    description: Optional referral code used during registration.
  - name: marketing_consent
    description: Boolean flag indicating if customer consented to marketing.

### stg_marketing_spend
**Description**: Daily marketing spend data, cleaned and typed for reporting by campaign, channel, and creative.
**Purpose**: Cleaned marketing spend data
**Key Columns**:
  - name: spend_date
    description: Date of the marketing spend.
  - name: channel
    description: Marketing channel used for the spend (e.g., google_search, email).
  - name: campaign_id
    description: Unique identifier of the marketing campaign.
  - name: campaign_name
    description: Descriptive name of the campaign.
  - name: ad_group
    description: The ad group within the campaign.
  - name: creative_type
    description: Type of creative used in the ad (e.g., text, carousel, story).
  - name: spend_amount
    description: Amount spent on the campaign on the given date (in dollars).
  - name: impressions
    description: Number of impressions recorded.
  - name: clicks
    description: Number of clicks recorded.

### stg_transactions
**Description**: Typed and cleaned transactional data, including product, payment, and attribution details. This model ensures consistent formatting and prepares raw seed data for use in marts.
**Purpose**: Cleaned transaction data
**Key Columns**:
  - name: transaction_id
    description: Unique identifier for each transaction.
  - name: order_id
    description: Identifier of the order (can group multiple transactions).
  - name: transaction_time
    description: Timestamp when the transaction was completed.
  - name: customer_id
    description: Customer who made the transaction.
  - name: product_id
    description: Unique identifier for the purchased product.
  - name: product_name
    description: Name of the purchased product.
  - name: category_id
    description: Product category ID.
  - name: category_name
    description: Descriptive name of the product category.
  - name: quantity
    description: Number of units purchased.
  - name: unit_price
    description: Price per unit of the product at transaction time.
  - name: discount_amount
    description: Total discount applied to the transaction.
  - name: shipping_cost
    description: Cost of shipping associated with the transaction.
  - name: tax_amount
    description: Tax amount charged.
  - name: total_amount
    description: Final total amount for the transaction.
  - name: payment_method
    description: Payment method used (e.g., credit_card, paypal).
  - name: device_type
    description: Type of device used to complete the transaction (e.g., mobile, desktop).
  - name: session_id
    description: Session identifier associated with the transaction.
  - name: utm_source
    description: UTM source used in the session, if available.
  - name: utm_medium
    description: UTM medium used in the session, if available.
  - name: utm_campaign
    description: UTM campaign identifier.
  - name: utm_content
    description: UTM content label.
  - name: is_first_purchase
    description: Boolean flag indicating whether this was the customer's first purchase.
  - name: days_since_first_visit
    description: Days since the user's first known session.
  - name: days_since_account_creation
    description: Number of days between account creation and transaction date.

### stg_website_events
**Description**: Cleaned and standardized website event logs, including page interactions, sessions, and UTM attribution. This model prepares the data for funnel analysis and attribution modeling.
**Purpose**: Cleaned website interaction events
**Key Columns**:
  - name: event_id
    description: "Unique identifier for each event."
  - name: event_time
    description: "Timestamp when the event occurred."
  - name: session_id
    description: "Identifier of the user's session during the event."
  - name: user_id
    description: "Identifier of the user performing the action."
  - name: page_url
    description: "The full URL of the page where the event occurred."
  - name: event_type
    description: "Type of interaction (e.g., page_view, cart_view, checkout_start, product_view)."
  - name: device_type
    description: "Device used to perform the event (e.g., mobile, desktop)."
  - name: utm_source
    description: "UTM source used in the session, if available."
  - name: utm_medium
    description: "UTM medium used in the session, if available."
  - name: utm_campaign
    description: "UTM campaign associated with the session."
  - name: utm_content
    description: "UTM content describing the ad variation."
  - name: product_id
    description: "ID of the product involved in the event, if applicable."
  - name: category_id
    description: "Product category associated with the event, if applicable."

