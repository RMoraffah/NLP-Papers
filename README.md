# Phase 2: Automated Data Creation 

### Diagram of Distribution
| Name | Dataset directory | Specification
| --- | --- | --- |
| Ujun Jeong | /coreference_data | Coreference Resolution |
| Jordan Miller| /SequentialDataset | Sequential Time Inference |
| John Cava| /Property_Questions | Property Inference |
| Raha Moraffah| /Causality Questions | Causal relationship Inference |
|Nick Dodd | /unanswerable_qa| Unanswerable Question Inference |
+ You can recreate data by using programs in /Codes directory

## Dataset Description
### Individual Dataset Descriptions
Ujun : Coreference data is made up with two part (extracted, generated), and each part has total 10K
+ <code>In extracted directory</code>, Context/Question/Answer is extracted from [NarrativeQA](https://github.com/vjg28/BERT_on_NarrativeQA)
+ In generated directory, Context is generation of contexts in NarrativeQA with [ILM model](https://github.com/chrisdonahue/ilm)
+ In generated directory, Question is back-translation of questions in NarrativeQA with [Google Translator](https://pypi.org/project/googletrans/)

Jordan : data is from SwagAF dataset (http://rowanzellers.com/swag/)
+ 10K QA were extracted for sequential time reseasoning
+ Context, Question, and Answer were extracted
+ Context was created using backtranslation with Google Translator
+ Questions and answers were left in the orginal langauge
  + This is due to Questions being very short, some even one word. 

John : property inference questions are based upon (belief states and property states)
+ A subset of data were extracted both from Cosmos and Quoref
+ A script was used to sift through a subset of these questions in respect to belief states and property states
+ Context, Question, and Answer were extracted. One of the datasets, had only A and B. A and B answers were backtranslated in order to create C and D
+ Context Was backtranslated to create a synthetic dataset, then from that the question aspect were backtranslated to create another dataset
 
Raha Moraffah: Task: Generating Causality data
+ Causality data have been generation by performing back-translation on the context of the datasets extracted from MC-Test data [1] and Cosmos data [2].
+ The data contains 10313 QA samples, where 10k are extracted from Cosmos data which is specifically designed for causality questions and 313 samples are extracted from MC-Test data by filtering the "Why type" questions.
+ The Context of the questions has been changed by applying back-translation on it using Google Translator API. 
+ Backtranslation is performed by first translating the context into a target domain (for instance persian) and then translating it back to the source domain (which is english)
+ The individual datasets designed for causality questions are in Causality Questions directory. The Causality_Data_Cosmos.json contains 10k data which are created by transforming Cosmos dataset. The Causality_Data_MC.json contains the transformed MC-Test dataset and the Causality_Data_Final.json contains the aggregated data by transforming both Cosmos and MC-Test datasets.

Nick Dodd: Task: Unanswerable Questions
+ Relevant data and code can be found under the unanswerable_qa directory.

+ To recreate, first clone or download: https://github.com/vsuthichai/paraphraser/tree/master . I structured the project as: data_gen-->models-->paraphraser-->paraphraser and will refer to these file paths throughout the rest of these notes.

+ Download the pre-trained model and extract the checkpoint files. The location is arbitrary as it will just be passed in as a sys arg when running the modified inference script. I staged the pre-trained model checkpoint files under data_gen-->models-->paraphraser-->trained_model_checkpoints-->train-20180325-001253

+ Next we need to download the Paraphrastic Sentence (para-nmt) Embeddings. Create a new directory directly under data_gen-->models-->paraphraser named para-nmt-50m. Download the embeddings from (https://drive.google.com/u/0/uc?id=1l2liCZqWX3EfYpzv9OmVatJAEISPFihW&export=download) and extract them in this newly created directory.

+ Due to outdated API and non-backwards compatibility of tensorflow, we will need to install some specific tool chains in order to get this model running. To isolate the toolchain from the other models, start by creating a new virtual environment by choosing a Python interpreter and making a .\venv directory to hold it. For example: C:\Users\nickg\Documents\cse576\project\data_gen\models\paraphraser>python -m venv --system-site-packages paraphraser_venv

+ Activate the virtual environment: C:\Users\nickg\Documents\cse576\project\data_gen\models\paraphraser>paraphraser_venv\Scripts\activate

+ Navigate to paraphraser root. (i.e. cd C:\Users\nickg\Documents\cse576\project\data_gen\models\paraphraser) Install python 3.6, I specifically used Python 3.6.8 Install tensorflow, spacy, and download the engligh language model for spacy: pip install --upgrade tensorflow==1.4.0 pip install spacy python -m spacy download en

+ Run the modified inference python script, using the checkpoint files to load the trained model: In data_gen/models/paraphraser/paraphraser/python, run python inference.py <path_to_trained_model_checkpoint> For example: python inference.py --checkpoint=C:\Users\nickg\Documents\cse576\project\data_gen\models\paraphraser\trained_model_checkpoints\train-20180325-001253\model-171856

+ The original script from the paraphraser model repo takes input from the command line and generates a fixed number of paraphrases at a fixed sampling temperature interactively. For our purposes, I built custom data handlers that loads and stages the parsed (question, context, answer-list) triplets of our datasets. For each data source, thre are methods which are used to determine the subspan to paraphrase for each element in the triplet. The data handler then handles generating the subspan paraphrases accordingly for each QA entity in the parsed dataset. Parsed datasets can be found in the data_gen/datasets directory.

+ Currently, there is a gap in the research community concerning multiple choice datasets that incorporate unanswerable questions. In fact, the vast majority of the publicly available datasets currently do not contain unanswerable questions, and the few that do are mostly developed for Extractive QA tasks. The one exception to this norm is in the CosmosQA dataset, where roughly 6.7% of the questions are unanswerable. Parsing for these questions can be found in the data_gen/datasets/cosmos_qa directory. Another multiple choice dataset that has unanswerable questions is the ComQA dataset, however since this dataset was developed for open domain question answering and lacks context paragraphs, it has not been included at this stage of the project. More research would be needed on how to best leverage information retrieval systems to create relevant context paragraphs for this dataset. Finally, SQUAD 2.0, the canonical dataset for unanswerable questions and the one that popularized the use of them in the QA and RC research community, was developed for extractive QA tasks, and thus doesn't contain a list of multiple answer choices, making it unusable as-is for our multiple choice question dataset. However, recent work in distractor generation (the generation of artificial answer choices in MCQ generation) seems to be a promising approach that could be leveraged to create multiple choice questions from this dataset by generating distractors (plausible answers) given context-question pairs. Towards this end, and to enable the use of SQUAD 2.0 unanswerable questions in our synthetic dataset generation process, several recent systems for distrator generation were considered, which can be found in the data_gen/models directory. These systems are then used with the pre-processed and parsed unanswerable questions from SQUAD 2.0 in order create an augmented set of multiple choice questions that comply to our format. These questions are then consumed by the custom squad data handler, which is used to generate subspan paraphrases of the dataset.

+ A combined subsample of around 10k unanswerable questions resulting from these processes can be found in data_gen/datasets/unanswerable_qa.json

### Data Format
The aggregated dataset is stored in a json file. Each data instance consists of a context (in natural language form), a questions Q associated with the type of reasoning (R), 4 choices(C), and the correct answer. The format of each instance of the data is shown below.

    {
    Context : ,
    Question: ,
    Reasoning type:,
    Choices: {A:, B:, C:, D:},
    Answer : 
    }

### Final dataset can be found at: https://drive.google.com/drive/folders/1m_xmnU3XAKvzLStDeqtW3dee6KXU9s9U?usp=sharing


## Task Distribution
- We each were to extract 10K datapoints from different datasets so we can build a robust model. 
- Each member was in charge of creating the dataset for a specific reasoning task. In total, we cover five different types of reasoning. Each member's associated reasoning task is as follows:
  1.Text Based question: (1) temporal order, (2) coreference By Ujun Jeong
  2. Causality By Raha Moraffah
  3. Event inference:(1) subsequent state(2)event duration. By Jordan Miller
  4. Property inference: (1) entity properties (2) belief states. By John Cava
  5. Unanswerable question By Nick Dodd
  
  -Data Integration for all tasks is done by Raha Moraffah




## Code Instructions

+ Causality data generation: In order to run the codes for generating causality data the following packages need to be installed: google translate, Pandas, Json. The code for generating causality data is given in a Jupyter notebook file called Data_Prep_Causal.ipynb in Codes directory.

## References:
[1] Richardson, Matthew, Christopher JC Burges, and Erin Renshaw. "Mctest: A challenge dataset for the open-domain machine comprehension of text." Proceedings of the 2013 Conference on Empirical Methods in Natural Language Processing. 2013.

[2] Huang, Lifu, et al. "Cosmos qa: Machine reading comprehension with contextual commonsense reasoning." arXiv preprint arXiv:1909.00277 (2019).

[3] Donahue, Chris, Mina Lee, and Percy Liang. "Enabling Language Models to Fill in the Blanks." arXiv preprint arXiv:2005.05339 (2020).

[4] Kočiský, Tomáš, et al. "The narrativeqa reading comprehension challenge." Transactions of the Association for Computational Linguistics 6 (2018): 317-328.

