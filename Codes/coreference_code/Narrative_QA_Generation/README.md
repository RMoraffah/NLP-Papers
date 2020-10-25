Instruction
-----------------------
**Context Generation**
1. run ./code_context_generation/generator.sh
2. It will output generated context in ./code_context_generation/data/curation
3. There will be two outputs : train_c.txt, valid_c.txt

**Question Backtranslation**
1. run ./code_question_backtranslation/back_translation.py
2. It will output new questions in ./code_question_backtranslation
3. There will be two outputs : train_q.txt, valid_q.txt

**Merging new data**
1. put train.json and valid.json in this directory (which is output of extracted NarrativeQA)
2. put train_c.txt and valid_c.txt in this directory (which is output of generated context)
3. put train_q.txt and valid_q.txt in this directory (which is output of backtranslation question)
4. run merge_genbacktranslation.py
5. There will be two outputs : train_gen.json, valid_gen.json

