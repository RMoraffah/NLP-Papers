# Phase 2: Automated Data Creation 

## Dataset Description
### Individual Dataset Descriptions
Ujun : coreference data is made up with two part (extracted, generated). Each part has a total of 9K train and 1K dev
+ In extracted directory, Context/Question/Answer is extracted from NarrativeQA 
+ In generated directory, Context is generated text of NarrativeQA with ILM model
+ In generated directory, Question is back-translated text of NarrativeQA with Google Translator

Jordan : data is from SwagAF dataset (http://rowanzellers.com/swag/)
+ 10K QA were extracted for sequential time reseasoning
+ Context, Question, and Answer were extracted
+ Context was created using backtranslation with Google Translator
+ Questions and answers were left in the orginal langauge
  + This is due to Questions being very short, some even one word. 

Raha Moraffah: Task: Generating Causality data
+ Causality data have been generation by performing back-translation on the context of the datasets extracted from MC-Test data [1] and Cosmos data [2].
+ The data contains 10313 QA samples, where 10k are extracted from Cosmos data which is specifically designed for causality questions and 313 samples are extracted from MC-Test data by filtering the "Why type" questions.
+ The Context of the questions has been changed by applying back-translation on it using Google Translator API. 
+ Backtranslation is performed by first translating the context into a target domain (for instance persian) and then translating it back to the source domain (which is english)
+ The individual datasets designed for causality questions are in Causality Questions directory. The Causality_Data_Cosmos.json contains 10k data which are created by transforming Cosmos dataset. The Causality_Data_MC.json contains the transformed MC-Test dataset and the Causality_Data_Final.json contains the aggregated data by transforming both Cosmos and MC-Test datasets.

### Data Format
The aggregated dataset consists of ...(Put the number here!) number of samples stored in a json file. Each data instance consists of a context (in natural language form), a questions Q associated with the type of reasoning (R), 4 choices(C), and the correct answer. The format of each instance of the data is shown below.

{

Context : ,

Question: ,

Reasoning type:,

Choices: {A:, B:, C:, D:},

Answer : 

}

The dataset contains data for 5 reasoning tasks as follows:

1. Text Based question: (1) temporal order, (2) coreference
2. Causality 
3. Event inference:(1) subsequent state(2)event duration.
4. Property inference: (1) entity properties (2) belief states.
5. Unanswerable question





## Task Distribution
- We each were to extract 10K datapoints from different datasets so we can build a robust model. 
- Each member was in charge of creating the dataset for a specific reasoning task. In total, we cover five different types of reasoning. Each member's associated reasoning task is as follows:
  1.Text Based question: (1) temporal order, (2) coreference By Ujun Jeong
  2. Causality By Raha Moraffah
  3. Event inference:(1) subsequent state(2)event duration. By Jordan Miller
  4. Property inference: (1) entity properties (2) belief states. By John Cava
  5. Unanswerable question By Nick Dodd




## Code Instructions

+ Causality data generation: In order to run the codes for generating causality data the following packages need to be installed: google translate, Pandas, Json. The code for generating causality data is given in a Jupyter notebook file called Data_Prep_caiusal.ipynb in Codes directory.

## References:
[1] Richardson, Matthew, Christopher JC Burges, and Erin Renshaw. "Mctest: A challenge dataset for the open-domain machine comprehension of text." Proceedings of the 2013 Conference on Empirical Methods in Natural Language Processing. 2013.

[2] Huang, Lifu, et al. "Cosmos qa: Machine reading comprehension with contextual commonsense reasoning." arXiv preprint arXiv:1909.00277 (2019).

