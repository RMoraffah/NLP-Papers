# Phase 2: Automated Data Creation 

## Dataset Description

Ujun : coreference data is made up with two part (extracted, generated). Each part has a total of 9K train and 1K dev
+ In extracted directory, Context/Question/Answer is extracted from NarrativeQA 
+ In generated directory, Context is generated text of NarrativeQA with ILM model
+ In generated directory, Question is back-translated text of NarrativeQA with Google Translator

Jordan : data is from SwagAF dataset (http://rowanzellers.com/swag/)
+ 10K QA were extracted for sequential time reseasoning
+ Context, Question, and Answer were extracted
+ Context was created using backtranslation with Google Translator
+ Questions and answers were left in the orginally langauge
  + This is due to Questions being very short, some even one word. 


## Task Distribution
- We each were to extract 10K datapoints from different datasets so we can build a robust model



## Code Instructions


