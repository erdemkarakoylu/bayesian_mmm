# Marketing Mix Model (MMM) Repository

This repository contains code and resources for implementing Marketing Mix Models (MMMs). MMMs are statistical models used to evaluate the effectiveness of marketing investments and optimize marketing spend.

## Types of MMMs

The basic principle of relating marketing inputs to sales remains the same, but MMMs can differ significantly in their structure and methodology. Here's a breakdown of some key dimensions along which MMMs can vary:

* **Statistical Approach:**

    * **Frequentist vs. Bayesian:** Models can use different statistical approaches. Traditional MMMs often use frequentist regression techniques, while more recent approaches, like the one in this repository, use Bayesian methods.

    * **Econometric vs. Statistical:** Some MMMs are heavily influenced by econometrics, focusing on causal inference and satisfying economic assumptions. Others are more statistically oriented, emphasizing prediction accuracy.

* **Model Structure:**

    * **Linear vs. Non-linear:** The relationship between marketing and sales can be modeled as linear or non-linear. Non-linear models can capture diminishing returns or saturation effects more effectively.

    * **Additive vs. Multiplicative:** In an additive model, the effects of different channels are added together. In a multiplicative model, they are multiplied. Multiplicative models are often used to represent interactions between channels.

    * **With or without Interaction Effects:** Some models include interaction terms to capture how the effect of one channel might depend on the level of spending in another.

* **Time Dependence:**

    * **Static vs. Dynamic:** Static models assume that the effect of marketing is immediate, while dynamic models incorporate lagged effects (like the adstock transformation) to account for how marketing's influence persists over time.

* **Level of Aggregation:**

    * **Aggregate vs. Disaggregate:** Most MMMs operate at an aggregate level (e.g., weekly sales), but some can incorporate more granular data, such as regional or even customer-level information.

* **Media Effects Modeling:**

    * **Adstock vs. Other Transformations:** While adstock is common, other transformations can be used to model media effects, such as the Hill function or other custom decay functions.

## Model in This Repository

The MMM implemented in this repository has the following characteristics:

* Bayesian
* Statistical
* Non-linear (due to the log transformation of spend)
* Additive
* Dynamic (due to the adstock transformation)
* Aggregate
