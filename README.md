# Data Exploration

## Download data
Download the data set from [https://www.kaggle.com/tuananhkk/lending-club-data-insights/data] and unzip in the `data/` directory.

## Running Instructions
For better portability, analysis is run in a Jupyter notebook within a docker container, specifically built off of the Jupyter/scipy-notebook image. Make sure Docker is installed on your machine following instructions listed [here](https://docs.docker.com/install/), then follow the instructions below.

1) The Makefile will start a Docker container based on the Jupyter/scipy-notebook image for you. Within the project root directory execute
```
Make
```

2) I've specified that the Docker start with a bash prompt, since we need to provide some additional settings to start up the Jupyter notebook with enough IO. At the prompt within the container, execute the below command to spin up the Jupyter notebook server.
```
jupyter notebook --NotebookApp.iopub_data_rate_limit=10000000
```

3) You'll see a URL printed in the logs. Copy _only_ the token that's printed to your clipboard. For example, from the following URL
```
http://74843c610200:8888/?token=36d1ce68c133f27715363061809701e77b3345ab973e6a35&token=36d1ce68c133f27715363061809701e77b3345ab973e6a35
```
you want only `36d1ce68c133f27715363061809701e77b3345ab973e6a35`.

4) Switch over to a browser, and visit [http://localhost:10000/]. Paste the token into the `Password or Token:` field.

5) Within the Jupyter interface, navigate to: `lendingclub/notebooks/` and select the notebook you would like to view. Initial exploration, cleanup and business analysis are in `1_Exploration` and modeling is in `3_modeling`

## Results

### Part 1: Data Exploration and Evaluation
To begin, I reviewed the data dictionary provided with the data set and searched [Lending Club](https://www.lendingclub.com/investing/investor-education) and other documentation to familiarize myself with any new terms. I then started classifying data elements into a few broad categories:
* demographic information (demographics)
* loan information (loan)
* credit information (credit)
* calculated by LC (LC_calcs)
* loan outcomes (outcomes)

Demographic and requested loan information are provided by the applicant on the application. Lending Club then obtains the applicant's credit information from credit bureaus, including credit score, debt-to-income ratio, credit history length, and recent credit activity.

Lending Club uses information provided by the applicant and credit bureaus to conduct an initial credit screening, and then uses a proprietary scoring model to either decline the applicant or assign a Loan Grade, Sub-Grade, and interest rate [[source](https://www.lendingclub.com/foliofn/rateDetail.action)]. In the data set, I assigned these elements to the LC_calcs category.

Finally, the data set includes measures of performance, such as principal payments, interest payments, fees, and associated dates. I classified these data elements as loan outcomes.

There are a few data elements that have different names in the data dictionary and the SQLite database:
* `is_inc_v` appears to correspond to `verification_status`
* `verified_status_joint` appears to correspond to `verfication_status_joint`

For the above, I updated the data dictionary to reflect the contents of the database.

There are a few data elements listed in the dictionary that are missing from the SQLite database and the CSV file, namely
* `fico_range_high`
* `fico_range_low`
* `last_fico_range_high`
* `last_fico_range_low`

I removed these elements from the data dictionary.

There is a minor difference between the data contained in the CSV file and the SQlite file, namely there are four additional rows of data in the SQLite file that do not appear in the CSV file. For the purposes of this analysis, I ignore this difference and load data either from the CSV or SQLite file depending on performance requirements.

I included two plots visualizing the data using Seaborn in the Jupyter notebook, but most of my inspection used the [Facets library](https://pair-code.github.io/facets/), specifically my fork that I included as a submodule. Facets is designed to assist in feature engineering and displays basic summary statistics about each feature, such as percent missing, percent zero, min, max, median, and a histogram. I embedded the visualization in each Jupyter notebook and tweaked the data it displayed when I wanted to view a different subset of the data.

### Part 2: Business Analysis
The last issue date for any loans in the data set is December 2015 and the last payment date for any loans in the data set is January 2016, so we assume that's the last date that we have information about any payments. If we only include loans that have at least 36 months of data, then we need to cut off loans that were issued 36 months prior to December 2015, which is December 2012.

I subsetted the data to only loans with terms of 36 months which had an issue date (`issue_d`) of December 2012 or earlier.

There is occasionally a difference between the total funded amount and the amount funded by investors, and a corresponding difference in total payments and the total payments for investors. To simplify, I will assume we're only interested in total returns.

The formula I will use to calculate average rate of return for the portfolio consisting of the full data set is: (Total Income-Total Cost) / Total Cost

In this data set:
* Total Income = total_pymnts
* Total Cost = funded_amnt + collection_recovery_fee

The loans in my subset of data generated an average return of 8.77%.
 When bucketed by year of origination and grade, grade G loans originating in 2012 had the highest average rate of return, 19.74%.

### Part 3: Modeling
Logistic regression is a form of predictive modeling that is more easily understood by most business stakeholders because the impact of each feature on the outcome can be explained. I chose to build a logistic regression model, using recursive feature elimination with cross-fold validation to select which features to include in a model predicting default rate in loans in the 36-month data set.

This procedure identified 55 features to use in the model, specifically
```
['emp_length', 'dti', 'inq_last_6mths', 'pub_rec', 'total_acc',
       'int_rate', 'mths_since_last_record_missing', 'tot_coll_amt_missing',
       'tot_cur_bal_missing', 'total_rev_hi_lim_missing', 'emp_length_missing',
       'home_ownership_mortgage', 'home_ownership_other', 'purpose_car',
       'purpose_credit_card', 'purpose_debt_consolidation',
       'purpose_educational', 'purpose_major_purchase', 'purpose_medical',
       'purpose_moving', 'purpose_other', 'purpose_small_business',
       'purpose_wedding', 'grade_a', 'grade_b', 'grade_c', 'grade_d',
       'grade_e', 'grade_f', 'grade_g', 'initial_list_status_f',
       'sub_grade_a1', 'sub_grade_a2', 'sub_grade_a3', 'sub_grade_a4',
       'sub_grade_a5', 'sub_grade_b2', 'sub_grade_b3', 'sub_grade_b4',
       'sub_grade_c1', 'sub_grade_c2', 'sub_grade_c3', 'sub_grade_c4',
       'sub_grade_d1', 'sub_grade_d2', 'sub_grade_d3', 'sub_grade_d5',
       'sub_grade_e2', 'sub_grade_e4', 'sub_grade_f4', 'sub_grade_f5',
       'sub_grade_g5', 'verification_status_not_verified',
       'verification_status_source_verified', 'verification_status_verified']
```

The model based on these features is able to identify loans at risk of default, however its sensitivity appears low, as it only predicts 70 defaults in a data set that should contain over 5000.

There is some improvement in rate of return in a portfolio which avoids these loans, but it is slim: 1.5 basis points. I laid out several next steps in the Jupyter notebook, including some additional feature engineering to try out. In addition, tuning the scoring function in the recursive feature selection would probably also help improve the sensitivity and specificity of the model.